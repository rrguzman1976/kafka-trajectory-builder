-- Create the test database
CREATE DATABASE ScratchDB;
GO

USE ScratchDB;
GO

EXEC sys.sp_cdc_enable_db;
GO

IF OBJECT_ID(N'dbo.DirectionalSurvey', N'U') IS NOT NULL
    DROP TABLE dbo.DirectionalSurvey;
GO

CREATE TABLE dbo.DirectionalSurvey
(
    SurveyId            INT             NOT NULL
        PRIMARY KEY,
    API                 VARCHAR(20)     NULL,
    WKID                VARCHAR(32)     NULL,
    FIPSCode            VARCHAR(4)      NULL,
    StatusCode          VARCHAR(1)      NOT NULL,
    Created             DATETIME2(7)    NOT NULL
        DEFAULT SYSUTCDATETIME()
);
GO

IF OBJECT_ID(N'dbo.SurveyReport', N'U') IS NOT NULL
    DROP TABLE dbo.SurveyReport;
GO

CREATE TABLE dbo.SurveyReport
(
    SurveyReportID      INT             NOT NULL
        PRIMARY KEY,
    DirectionalSurveyId INT             NOT NULL
        FOREIGN KEY REFERENCES dbo.DirectionalSurvey (SurveyId),
    Azimuth             FLOAT           NULL,
    MD                  FLOAT           NULL,
    TVD                 FLOAT           NULL,
    Inclination         FLOAT           NULL,
    StatusCode          VARCHAR(1)      NOT NULL,
    Created             DATETIME2(7)    NOT NULL
        DEFAULT SYSUTCDATETIME()
);
GO

CREATE TABLE dbo.DbzWell
(
  --WellId        BIGINT          NOT NULL
  API           VARCHAR(20)     NOT NULL
    PRIMARY KEY
  , WellName    VARCHAR(255)    NOT NULL
  , Latitude    FLOAT           NOT NULL
  , Longitude   FLOAT           NOT NULL
  , ts          DATETIME2(2)    NOT NULL
      DEFAULT SYSUTCDATETIME()
);
GO

EXEC sys.sp_cdc_enable_table 
    @source_schema = 'dbo'
    , @source_name = 'DbzWell'
    , @role_name = NULL
    , @supports_net_changes = 0;
GO

INSERT INTO dbo.DirectionalSurvey (
    [SurveyId]
    ,[API]
    ,[WKID]
    ,[FIPSCode]
    ,[StatusCode]
    --,[Created]
)
VALUES (1, '00-000-00001', 'WKID1', '0001', 'N')
        , (2, '00-000-00002', 'WKID2', '0002', 'C')
        , (3, '00-000-00003', 'WKID3', '0003', 'N');
GO

INSERT INTO dbo.SurveyReport (
    [SurveyReportID]
    ,[DirectionalSurveyId]
    ,[Azimuth]
    ,[MD]
    ,[TVD]
    ,[Inclination]
    ,[StatusCode]    
)
VALUES (1, 1, 1.0, 2.0, 21.0, 3.0, 'N')
        , (2, 1, 4.0, 5.0, 21.0, 6.0, 'C')
        , (3, 2, 7.0, 8.0, 21.0, 9.0, 'N')
        , (4, 2, 1.0, 2.0, 21.0, 3.0, 'N')
        , (5, 3, 4.0, 5.0, 21.0, 6.0, 'C')
        , (6, 3, 7.0, 8.0, 21.0, 9.0, 'N');
GO

INSERT INTO dbo.DbzWell (API, WellName, Latitude, Longitude)
  VALUES ('00-000-00000', 'WELL-0', 31.8457, 102.3676)
          , ('00-000-00001', 'WELL-1', 31.8457, 102.3676)
          , ('00-000-00002', 'WELL-2', 31.8457, 102.3676)
          , ('00-000-00003', 'WELL-3', 31.8457, 102.3676)
          , ('00-000-00004', 'WELL-4', 31.8457, 102.3676)
          , ('00-000-00005', 'WELL-5', 31.8457, 102.3676)
          , ('00-000-00006', 'WELL-6', 31.8457, 102.3676)
          , ('00-000-00007', 'WELL-7', 31.8457, 102.3676)
          , ('00-000-00008', 'WELL-8', 31.8457, 102.3676)
          , ('00-000-00009', 'WELL-9', 31.8457, 102.3676)
          , ('00-000-00010', 'WELL-NAME-10', 31.8457, 102.3676)
          , ('00-000-00011', 'WELL-NAME-11', 31.8457, 102.3676)
          , ('00-000-00012', 'WELL-NAME-12', 31.8457, 102.3676)
          , ('00-000-00013', 'WELL-NAME-13', 31.8457, 102.3676)
          , ('00-000-00014', 'WELL-NAME-14', 31.8457, 102.3676)
          , ('00-000-00015', 'WELL-NAME-15', 31.8457, 102.3676)
          , ('00-000-00016', 'WELL-NAME-16', 31.8457, 102.3676)
          , ('00-000-00017', 'WELL-NAME-17', 31.8457, 102.3676)
          , ('00-000-00018', 'WELL-NAME-18', 31.8457, 102.3676)
          , ('00-000-00019', 'WELL-NAME-19', 31.8457, 102.3676)
          , ('00-000-00020', 'WELL-NAME-20', 31.8457, 102.3676)
          , ('00-000-00021', 'WELL-NAME-21', 31.8457, 102.3676)
          , ('00-000-00022', 'WELL-NAME-22', 31.8457, 102.3676)
          , ('00-000-00023', 'WELL-NAME-23', 31.8457, 102.3676)
          , ('00-000-00024', 'WELL-NAME-24', 31.8457, 102.3676)
;
GO
