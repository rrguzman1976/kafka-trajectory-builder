package com.github.rrguzman1976.kafka.serdes;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectReader;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

import java.io.IOException;
import java.util.Map;

/* Generic class to handle Debezium change data stream.
 * See https://github.com/debezium/debezium-examples/tree/master/kstreams-live-update
 */
public class DebeziumJSONSerde<T> implements Serde<T> {

    private final ObjectMapper mapper;
    private final ObjectReader reader;
    private boolean isKey;

    public DebeziumJSONSerde(Class<T> objectType) {
        mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());

        this.reader = mapper.readerFor(objectType);
    }

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
        this.isKey = isKey;
    }

    @Override
    public void close() {
    }

    @Override
    public Serializer<T> serializer() {
        return new JsonSerializer();
    }

    @Override
    public Deserializer<T> deserializer() {
        return new JsonDeserializer();
    }

    private final class JsonDeserializer implements Deserializer<T> {

        @Override
        public void configure(Map<String, ?> configs, boolean isKey) {
        }

        @Override
        public T deserialize(String topic, byte[] data) {
            if (data == null) {
                return null;
            }

            try {
                JsonNode node = mapper.readTree(data);

                if (isKey) {
                    if (node.isObject()) {
                        if (node.has("payload")) {
                            return reader.readValue(node.get("payload").get("API"));
                            //return reader.readValue(node.get("payload").get("id"));
                        }
                        else {
                            return reader.readValue(node.get("API"));
                            //return reader.readValue(node.get("id"));
                        }
                    }
                    else {
                        return reader.readValue(node);
                    }
                }
                else {
                    JsonNode payload = node.get("payload");
                    if (payload != null) {
                        return reader.readValue(payload.get("after"));
                    }
                    else {
                        if (node.has("before") && node.has("after") && node.has("source")) {
                            return reader.readValue(node.get("after"));
                        }
                        else {
                            return reader.readValue(node);
                        }
                    }
                }
            }
            catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        public void close() {
        }
    }

    private final class JsonSerializer implements Serializer<T> {

        @Override
        public void configure(Map<String, ?> configs, boolean isKey) {
        }

        @Override
        public byte[] serialize(String topic, T data) {
            try {
                return mapper.writeValueAsBytes(data);
            }
            catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        public void close() {
        }
    }
}
