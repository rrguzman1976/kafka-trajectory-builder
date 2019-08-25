package com.github.rrguzman1976.kafka.serdes;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.rrguzman1976.kafka.beans.DirectionalSurvey;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

import java.io.IOException;
import java.util.Map;

public class SurveyJSONSerde<T extends DirectionalSurvey>  implements Serializer<T>, Deserializer<T>, Serde<T> {
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    public SurveyJSONSerde() {}

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {}

    @Override
    public T deserialize(String s, byte[] bytes) {
        if (bytes == null) {
            return null;
        }

        try {
            return (T) OBJECT_MAPPER.readValue(bytes, DirectionalSurvey.class);
        } catch (IOException e) {
            throw new SerializationException("Error deserializing JSON message", e);
        }
    }

    @Override
    public byte[] serialize(String s, T bean) {
        if (bean == null) {
            return null;
        }

        try {
            return OBJECT_MAPPER.writeValueAsBytes(bean);
        } catch (final Exception e) {
            throw new SerializationException("Error serializing JSON message", e);
        }
    }

    @Override
    public void close() {}

    @Override
    public Deserializer<T> deserializer() {
        return this;
    }

    @Override
    public Serializer<T> serializer() {
        return this;
    }
}
