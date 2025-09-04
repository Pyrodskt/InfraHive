
GO
SET ANSI_NULLS, ANSI_PADDING, ANSI_WARNINGS, ARITHABORT, CONCAT_NULL_YIELDS_NULL, QUOTED_IDENTIFIER ON;

SET NUMERIC_ROUNDABORT OFF;


GO
:setvar DatabaseName "KPI_HOSTING"
:setvar DefaultFilePrefix "KPI_HOSTING"
:setvar DefaultDataPath ""
:setvar DefaultLogPath ""

GO
:on error exit
GO
/*
Détectez le mode SQLCMD et désactivez l'exécution du script si le mode SQLCMD n'est pas pris en charge.
Pour réactiver le script une fois le mode SQLCMD activé, exécutez ce qui suit :
SET NOEXEC OFF; 
*/
:setvar __IsSqlCmdEnabled "True"
GO
IF N'$(__IsSqlCmdEnabled)' NOT LIKE N'True'
    BEGIN
        PRINT N'Le mode SQLCMD doit être activé de manière à pouvoir exécuter ce script.';
        SET NOEXEC ON;
    END


GO
USE [master];


GO

IF (DB_ID(N'$(DatabaseName)') IS NOT NULL) 
BEGIN
    ALTER DATABASE [$(DatabaseName)]
    SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [$(DatabaseName)];
END

GO
PRINT N'Création de la base de données $(DatabaseName)...'
GO
CREATE DATABASE [$(DatabaseName)] COLLATE SQL_Latin1_General_CP1_CI_AS
GO
USE [$(DatabaseName)];


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET ANSI_NULLS ON,
                ANSI_PADDING ON,
                ANSI_WARNINGS ON,
                ARITHABORT ON,
                CONCAT_NULL_YIELDS_NULL ON,
                NUMERIC_ROUNDABORT OFF,
                QUOTED_IDENTIFIER ON,
                ANSI_NULL_DEFAULT ON,
                CURSOR_DEFAULT LOCAL,
                RECOVERY FULL,
                CURSOR_CLOSE_ON_COMMIT OFF,
                AUTO_CREATE_STATISTICS ON,
                AUTO_SHRINK OFF,
                AUTO_UPDATE_STATISTICS ON,
                RECURSIVE_TRIGGERS OFF 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET ALLOW_SNAPSHOT_ISOLATION OFF;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET READ_COMMITTED_SNAPSHOT OFF 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET AUTO_UPDATE_STATISTICS_ASYNC OFF,
                PAGE_VERIFY NONE,
                DATE_CORRELATION_OPTIMIZATION OFF,
                DISABLE_BROKER,
                PARAMETERIZATION SIMPLE,
                SUPPLEMENTAL_LOGGING OFF 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF IS_SRVROLEMEMBER(N'sysadmin') = 1
    BEGIN
        IF EXISTS (SELECT 1
                   FROM   [master].[dbo].[sysdatabases]
                   WHERE  [name] = N'$(DatabaseName)')
            BEGIN
                EXECUTE sp_executesql N'ALTER DATABASE [$(DatabaseName)]
    SET TRUSTWORTHY OFF,
        DB_CHAINING OFF 
    WITH ROLLBACK IMMEDIATE';
            END
    END
ELSE
    BEGIN
        PRINT N'Impossible de modifier les paramètres de base de données. Vous devez être administrateur système pour appliquer ces paramètres.';
    END


GO
IF IS_SRVROLEMEMBER(N'sysadmin') = 1
    BEGIN
        IF EXISTS (SELECT 1
                   FROM   [master].[dbo].[sysdatabases]
                   WHERE  [name] = N'$(DatabaseName)')
            BEGIN
                EXECUTE sp_executesql N'ALTER DATABASE [$(DatabaseName)]
    SET HONOR_BROKER_PRIORITY OFF 
    WITH ROLLBACK IMMEDIATE';
            END
    END
ELSE
    BEGIN
        PRINT N'Impossible de modifier les paramètres de base de données. Vous devez être administrateur système pour appliquer ces paramètres.';
    END


GO
ALTER DATABASE [$(DatabaseName)]
    SET TARGET_RECOVERY_TIME = 0 SECONDS 
    WITH ROLLBACK IMMEDIATE;


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET FILESTREAM(NON_TRANSACTED_ACCESS = OFF),
                CONTAINMENT = NONE 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET AUTO_CREATE_STATISTICS ON(INCREMENTAL = OFF),
                MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = OFF,
                DELAYED_DURABILITY = DISABLED 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET QUERY_STORE (QUERY_CAPTURE_MODE = ALL, DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_PLANS_PER_QUERY = 200, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 367), MAX_STORAGE_SIZE_MB = 100) 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE [$(DatabaseName)]
            SET QUERY_STORE = OFF 
            WITH ROLLBACK IMMEDIATE;
    END


GO
IF EXISTS (SELECT 1
           FROM   [master].[dbo].[sysdatabases]
           WHERE  [name] = N'$(DatabaseName)')
    BEGIN
        ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
        ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = PRIMARY;
        ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
        ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET LEGACY_CARDINALITY_ESTIMATION = PRIMARY;
        ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
        ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET PARAMETER_SNIFFING = PRIMARY;
        ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
        ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET QUERY_OPTIMIZER_HOTFIXES = PRIMARY;
    END


GO
IF fulltextserviceproperty(N'IsFulltextInstalled') = 1
    EXECUTE sp_fulltext_database 'enable';

-- Tables de référence
CREATE TABLE dbo.operating_system (
  id_Operating_System INT IDENTITY(1,1) PRIMARY KEY,
  os_name VARCHAR(75) NULL,
  os_description VARCHAR(255) NULL
);

CREATE TABLE dbo.application (
  id_application INT IDENTITY(1,1) PRIMARY KEY,
  app_name VARCHAR(100) NULL,
  app_code VARCHAR(10) NULL,
  app_owner VARCHAR(100) NULL
);

CREATE TABLE dbo.server_role (
  id_server_role INT IDENTITY(1,1) PRIMARY KEY,
  role_code VARCHAR(45) NULL,
  role_description VARCHAR(100) NULL
);

CREATE TABLE dbo.server_tier (
  id_tier INT IDENTITY(1,1) PRIMARY KEY,
  tier_name VARCHAR(45) NULL
);

CREATE TABLE dbo.server_source (
  id_source INT IDENTITY(1,1) PRIMARY KEY,
  source_name VARCHAR(45) NULL,
  source_description VARCHAR(100) NULL
);

CREATE TABLE dbo.vinci_division (
  id_vinci_division INT IDENTITY(1,1) PRIMARY KEY,
  division_name VARCHAR(255) NULL,
  division_code VARCHAR(255) NULL
);

CREATE TABLE dbo.environnement (
  id_environnement INT IDENTITY(1,1) PRIMARY KEY,
  env_name VARCHAR(45) NULL,
  env_code VARCHAR(45) NULL
);

-- Cloud subscription
CREATE TABLE dbo.cloud_subscription (
  id_cloud_subscription INT IDENTITY(1,1) PRIMARY KEY,
  sub_name VARCHAR(100) NULL,
  sub_id VARCHAR(100) NULL,
  id_source INT NOT NULL,
  rg_name VARCHAR(100) NULL,
  id_vinci_division INT NOT NULL,
  id_environnement INT NOT NULL,
  id_tier INT NOT NULL,
  update_date DATE NULL DEFAULT GETDATE(),
  
  FOREIGN KEY (id_source) REFERENCES dbo.server_source(id_source),
  FOREIGN KEY (id_vinci_division) REFERENCES dbo.vinci_division(id_vinci_division),
  FOREIGN KEY (id_environnement) REFERENCES dbo.environnement(id_environnement),
  FOREIGN KEY (id_tier) REFERENCES dbo.server_tier(id_tier)
);

-- Serveurs
CREATE TABLE dbo.server (
  id_server INT IDENTITY(1,1) PRIMARY KEY,
  server_name VARCHAR(255) NULL,
  is_appliance BIT NULL,
  is_obsolete BIT NULL,
  power_state VARCHAR(50) NULL,
  r7_risk_score VARCHAR(45) NULL,
  id_operating_system INT NOT NULL,
  id_application INT NOT NULL,
  id_server_role INT NOT NULL,
  id_tier INT NOT NULL,
  id_source INT NOT NULL,
  id_cloud_subscription INT NULL,
  id_environnement INT NOT NULL,
  id_vinci_division INT NOT NULL,
  update_date DATE NULL DEFAULT GETDATE(),

  FOREIGN KEY (id_operating_system) REFERENCES dbo.operating_system(id_Operating_System),
  FOREIGN KEY (id_application) REFERENCES dbo.application(id_application),
  FOREIGN KEY (id_server_role) REFERENCES dbo.server_role(id_server_role),
  FOREIGN KEY (id_tier) REFERENCES dbo.server_tier(id_tier),
  FOREIGN KEY (id_source) REFERENCES dbo.server_source(id_source),
  FOREIGN KEY (id_cloud_subscription) REFERENCES dbo.cloud_subscription(id_cloud_subscription),
  FOREIGN KEY (id_environnement) REFERENCES dbo.environnement(id_environnement),
  FOREIGN KEY (id_vinci_division) REFERENCES dbo.vinci_division(id_vinci_division)
);

-- Réseau
CREATE TABLE dbo.network (
  id_network INT IDENTITY(1,1) PRIMARY KEY,
  subnet_name VARCHAR(255) NULL,
  vnet_name VARCHAR(255) NULL,
  is_dmz BIT NULL,
  id_vinci_division INT NOT NULL,
  FOREIGN KEY (id_vinci_division) REFERENCES dbo.vinci_division(id_vinci_division)
);

-- Agents
CREATE TABLE dbo.agents (
  id_agent INT IDENTITY(1,1) PRIMARY KEY,
  agent_name VARCHAR(45) NULL,
  agent_process_name VARCHAR(255) NULL,
  agent_type VARCHAR(45) NULL,
  agent_criticity VARCHAR(45) NULL,
  has_api BIT NULL
);

-- Liaison serveur <-> agent
CREATE TABLE dbo.server_has_agent (
  id_server_has_agent INT IDENTITY(1,1) PRIMARY KEY,
  id_server INT NOT NULL,
  id_agent INT NOT NULL,
  status BIT NULL,
  is_installable BIT NULL,
  is_required BIT NULL,
  update_date DATE NULL DEFAULT GETDATE(),
  comment VARCHAR(255) NULL,

  FOREIGN KEY (id_server) REFERENCES dbo.server(id_server),
  FOREIGN KEY (id_agent) REFERENCES dbo.agents(id_agent)
);

-- Patching
CREATE TABLE dbo.update_phase (
  id_update_phase INT IDENTITY(1,1) PRIMARY KEY,
  phase_name VARCHAR(255) NULL,
  phase_description VARCHAR(255) NULL,
  phase_next_period VARCHAR(255) NULL
);

CREATE TABLE dbo.patching (
  id_patching INT IDENTITY(1,1) PRIMARY KEY,
  status BIT NULL,
  id_server INT NOT NULL,
  id_update_phase INT NOT NULL,
  update_date DATE NULL DEFAULT GETDATE(),
  FOREIGN KEY (id_server) REFERENCES dbo.server(id_server),
  FOREIGN KEY (id_update_phase) REFERENCES dbo.update_phase(id_update_phase)
);

-- Liaison serveur <-> réseau
CREATE TABLE dbo.server_has_network (
  id_server_has_network INT IDENTITY(1,1) PRIMARY KEY,
  ip_address VARCHAR(255) NULL,
  id_network INT NOT NULL,
  id_server INT NOT NULL,
  FOREIGN KEY (id_network) REFERENCES dbo.network(id_network),
  FOREIGN KEY (id_server) REFERENCES dbo.server(id_server)
);
