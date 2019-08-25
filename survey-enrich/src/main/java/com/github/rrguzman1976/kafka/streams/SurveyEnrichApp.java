package com.github.rrguzman1976.kafka.streams;

import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;

import com.github.rrguzman1976.kafka.beans.DbzWell;
import com.github.rrguzman1976.kafka.serdes.DebeziumJSONSerde;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.KeyValueStore;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;

import com.github.rrguzman1976.kafka.beans.DirectionalSurvey;
import com.github.rrguzman1976.kafka.serdes.SurveyJSONSerde;

public class SurveyEnrichApp {
    // TODO: Setup logger level to debug.
    private static Logger logger = LoggerFactory.getLogger(SurveyEnrichApp.class.getName());

    public static void main(String[] args) {

        Properties config = new Properties();
        config.put(StreamsConfig.APPLICATION_ID_CONFIG, "survey-enrich-app");
        config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        config.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        //config.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class.getName());
        //config.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.StringSerde.class.getName());
        config.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, "0"); // Disable cache debug only - not PROD
        //config.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once"); // requires 3 brokers
        config.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, "1"); // per app

        String inputSurveyTopic = "survey-acq";
        String inputWellTopic = "funky-chicken.dbo.DbzWell";
        String outputTopic = "survey-cln";

        SurveyEnrichApp app = new SurveyEnrichApp();
        Topology topo = app.buildTopology(inputSurveyTopic, inputWellTopic, outputTopic);

        KafkaStreams streams = new KafkaStreams(topo, config);
        streams.cleanUp(); // clear local stores - only for debugging
        CountDownLatch latch = new CountDownLatch(1);

        logger.info("Printing topology: " + topo.describe());

        streams.setUncaughtExceptionHandler((Thread thread, Throwable throwable) -> {
            logger.error("Unknown error...", throwable.getMessage());
            streams.close();
            latch.countDown();
        });

        Runtime.getRuntime().addShutdownHook(new Thread(() ->
        {
            logger.info("Received shutdown signal...");
            streams.close();
            latch.countDown();
        }));

        try {
            streams.start();
            latch.await();
            logger.info("Turning off the lights...");
        } catch (final Throwable e) {
            logger.error("Unexpected error...", e);
            System.exit(1);
        }
        logger.info("Exiting...");
        System.exit(0);

    }

    private Topology buildTopology(String surveyTopic, String wellTopic, String outputTopic) {
        Serde<DirectionalSurvey> dsSerde = new SurveyJSONSerde<DirectionalSurvey>();

        Serde<String> keySerde = new DebeziumJSONSerde<>(String.class);
        keySerde.configure(Collections.emptyMap(), true);
        Serde<DbzWell> wellSerde = new DebeziumJSONSerde<>(DbzWell.class);
        wellSerde.configure(Collections.emptyMap(), false);

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, DirectionalSurvey> surveys = builder.stream(surveyTopic
                , Consumed.with(Serdes.String(), dsSerde));

        KStream<String, DirectionalSurvey> surveys_peek = surveys.peek((k, v) -> {
            logger.info(String.format("Key=%1$s, Survey=%2$s", k, v.API));
        });

        KTable<String, DbzWell> wells = builder.table(wellTopic
                , Consumed.with(keySerde, wellSerde)
                , Materialized.<String, DbzWell, KeyValueStore<Bytes, byte[]>> as("DbzWellStore"));

        // KStream-KTable left join (enrich with Well and WGS84 surface location)
        // TODO: Use global KTable
        KStream<Integer, DirectionalSurvey> enriched = surveys_peek
                .selectKey((k, v) -> v.API) // String key, previous was SurveyId
                .leftJoin(wells
                        , (v1, v2) -> { // ValueJoiner<v1, v2, returned>
                            logger.info(String.format("Join: (%1$s), (%2$s)", v1, v2));
                            if (v2 != null) { // left-join semantics
                                v1.WellName = v2.WellName;
                                v1.Latitude = v2.Latitude;
                                v1.Longitude = v2.Longitude;
                            }

                            return v1; // return enriched survey
                        }
                        // IMPORTANT: Provide specific instructions on serdes for both sides of the join.
                        , Joined.with(Serdes.String(), dsSerde, wellSerde)
                )
                .selectKey((k, v) -> v.SurveyId) // to SurveyId int key (previous was API)
                ;

        enriched.to(outputTopic, Produced.with(Serdes.Integer(), dsSerde));

        return builder.build();
    }
}
