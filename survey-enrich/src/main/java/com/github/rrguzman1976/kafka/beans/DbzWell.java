package com.github.rrguzman1976.kafka.beans;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.ZonedDateTime;

public class DbzWell {

    @JsonProperty("ts")
    public ZonedDateTime timestamp;

    @JsonProperty("API")
    public String API;

    @JsonProperty("WellName")
    public String WellName;

    @JsonProperty("Latitude")
    public double Latitude;

    @JsonProperty("Longitude")
    public double Longitude;

    DbzWell() {
    }

    public DbzWell(long id, String api, String wellname, double latitude
            , double longitude, ZonedDateTime timestamp) {
        this.timestamp = timestamp;
        this.API = api;
        this.WellName = wellname;
        this.Latitude = latitude;
        this.Longitude = longitude;
    }

    @Override
    public String toString() {
        return "Well [api=" + this.API + ", Well=" + this.WellName + "]";
    }
}
