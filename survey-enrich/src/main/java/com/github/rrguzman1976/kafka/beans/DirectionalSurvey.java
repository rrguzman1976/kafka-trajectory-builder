package com.github.rrguzman1976.kafka.beans;

import java.util.List;

public class DirectionalSurvey {

    public int SurveyId;
    public String API;
    public String WKID;
    public String FIPSCode;
    public String StatusCode;
    public String WellName;
    public double Latitude;
    public double Longitude;
    public String Created;

    public List<SurveyReport> Stations;

    public DirectionalSurvey() {}

    public DirectionalSurvey(List<SurveyReport> stations)
    {
        this.Stations = stations;
    }

    @Override
    public String toString() {
        return String.format("%1$d, %2$s, %3$s, %4$s, %5$+5.2f, %6$+5.2f"
                , SurveyId, API, WKID, WellName, Latitude, Longitude);
    }

}
