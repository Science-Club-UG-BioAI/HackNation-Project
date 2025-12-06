
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA ref');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'org') EXEC('CREATE SCHEMA org');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dim') EXEC('CREATE SCHEMA dim');


CREATE TABLE ref.BudgetPart (
    BudgetPartId INT IDENTITY PRIMARY KEY,
    PartCode VARCHAR(10) NOT NULL UNIQUE,
    ParentPartCode VARCHAR(10) NULL,
    Name NVARCHAR(255) NOT NULL,
    IsGroup BIT NOT NULL DEFAULT 0,
    ValidFrom DATE NOT NULL,
    ValidTo DATE NULL
);

CREATE TABLE ref.Dzial (
    DzialId INT IDENTITY PRIMARY KEY,
    DzialCode VARCHAR(10) NOT NULL UNIQUE,
    Name NVARCHAR(255) NOT NULL
);

CREATE TABLE ref.Rozdzial (
    RozdzialId INT IDENTITY PRIMARY KEY,
    RozdzialCode VARCHAR(10) NOT NULL UNIQUE,
    DzialId INT NOT NULL,
    Name NVARCHAR(255) NOT NULL,
    FOREIGN KEY (DzialId) REFERENCES ref.Dzial(DzialId)
);

CREATE TABLE ref.Paragraf (
    ParagrafId INT IDENTITY PRIMARY KEY,
    ParagrafCode VARCHAR(10) NOT NULL UNIQUE,
    Name NVARCHAR(255) NULL
);

CREATE TABLE ref.SourceOfFunding (
    SourceId INT IDENTITY PRIMARY KEY,
    SourceCode CHAR(1) NOT NULL UNIQUE,
    Name NVARCHAR(200) NOT NULL
);

CREATE TABLE ref.ExpenseGroup (
    ExpenseGroupId INT IDENTITY PRIMARY KEY,
    Name NVARCHAR(250) NOT NULL UNIQUE
);

CREATE TABLE ref.BudgetTask (
    BudgetTaskId INT IDENTITY PRIMARY KEY,
    FullCode VARCHAR(50) NOT NULL UNIQUE, 
    FunctionNo VARCHAR(10) NULL,
    TaskNo VARCHAR(10) NULL,
    Description NVARCHAR(400) NULL
);

CREATE TABLE ref.ProgramProject (
    ProgramId INT IDENTITY PRIMARY KEY,
    Name NVARCHAR(400) NOT NULL,
    SourceId INT NOT NULL,
    FOREIGN KEY (SourceId) REFERENCES ref.SourceOfFunding(SourceId)
);

CREATE TABLE org.OrganizationalUnit (
    OrgUnitId INT IDENTITY PRIMARY KEY,
    Code VARCHAR(50) NULL,
    Name NVARCHAR(400) NOT NULL
);

CREATE TABLE dim.Dysponent (
    DysponentId INT IDENTITY PRIMARY KEY,
    Name NVARCHAR(300) NOT NULL,
    Notes NVARCHAR(1000) NULL
);

CREATE TABLE dbo.Budget (
    BudgetId INT IDENTITY PRIMARY KEY,
    BudgetName NVARCHAR(300) NOT NULL,
    Version NVARCHAR(50) NULL,
    OwnerUser NVARCHAR(200) NULL,
    Status NVARCHAR(50) NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    Notes NVARCHAR(MAX) NULL,
    BudgetPartId INT NULL,
    FOREIGN KEY (BudgetPartId) REFERENCES ref.BudgetPart(BudgetPartId)
);

CREATE TABLE dbo.BudgetLine (
    BudgetLineId BIGINT IDENTITY PRIMARY KEY,
    BudgetGroupId UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    BudgetName NVARCHAR(250) NULL,
    Version NVARCHAR(50) NULL,
    OwnerUser NVARCHAR(200) NULL,


    BudgetPartId INT NULL,
    DzialId INT NULL,
    RozdzialId INT NULL,
    ParagrafId INT NULL,
    SourceId INT NULL,
    ExpenseGroupId INT NULL,
    BudgetTaskId INT NULL,
    ProgramId INT NULL,
    OrgUnitId INT NULL,
    DysponentId INT NULL,

    PlanWI DECIMAL(19,4) NULL,
    Amount DECIMAL(19,4) NOT NULL DEFAULT 0,
    Currency CHAR(3) NOT NULL DEFAULT 'PLN',

    TaskName NVARCHAR(400) NULL,
    DetailJustification NVARCHAR(MAX) NULL,

    ImportBatchId VARCHAR(100) NULL,
    RowNumberInSource INT NULL,
    IsLocked BIT NOT NULL DEFAULT 0,

    CreatedBy INT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    ModifiedAt DATETIME2 NULL,

    FOREIGN KEY (BudgetPartId) REFERENCES ref.BudgetPart(BudgetPartId),
    FOREIGN KEY (DzialId) REFERENCES ref.Dzial(DzialId),
    FOREIGN KEY (RozdzialId) REFERENCES ref.Rozdzial(RozdzialId),
    FOREIGN KEY (ParagrafId) REFERENCES ref.Paragraf(ParagrafId),
    FOREIGN KEY (SourceId) REFERENCES ref.SourceOfFunding(SourceId),
    FOREIGN KEY (ExpenseGroupId) REFERENCES ref.ExpenseGroup(ExpenseGroupId),
    FOREIGN KEY (BudgetTaskId) REFERENCES ref.BudgetTask(BudgetTaskId),
    FOREIGN KEY (ProgramId) REFERENCES ref.ProgramProject(ProgramId),
    FOREIGN KEY (OrgUnitId) REFERENCES org.OrganizationalUnit(OrgUnitId),
    FOREIGN KEY (DysponentId) REFERENCES dim.Dysponent(DysponentId)
);
'''
-- tabela M:N 
CREATE TABLE ref.PurposeArea (
    PurposeAreaId INT IDENTITY PRIMARY KEY,
    Code VARCHAR(50) NOT NULL UNIQUE,
    Name NVARCHAR(200) NOT NULL
);
'''
CREATE TABLE dbo.BudgetLine_PurposeArea (
    BudgetLineId BIGINT NOT NULL,
    PurposeAreaId INT NOT NULL,
    PRIMARY KEY (BudgetLineId, PurposeAreaId),
    FOREIGN KEY (BudgetLineId) REFERENCES dbo.BudgetLine(BudgetLineId),
    FOREIGN KEY (PurposeAreaId) REFERENCES ref.PurposeArea(PurposeAreaId)
);




