package com.github.rrguzman1976.kafka.beans;

import java.util.Date;

public class SurveyReport {
    public int SurveyReportID;
    public double Azimuth;
    public double MD;
    public double TVD;
    public double Inclination;
    public String StatusCode;
    public String Created;

    public SurveyReport() {}

    @Override
    public String toString() {
        return String.format("%1$d, %2$+5.2f, %3$+5.2f, %4$+5.2f, %5$+5.2f, %6$+5.2f"
                , SurveyReportID, Azimuth, MD, TVD, Inclination);
    }
}
