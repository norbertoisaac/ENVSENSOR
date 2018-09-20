/*
ENVSENSOR is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

ENVSENSOR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ENVSENSOR. If not, see https://www.gnu.org/licenses/.
*/
CREATE DATABASE envsensor;
-- Create role. User: envsysfe, password: %envT434%
-- echo -n "%envT434%envsysfe" | md5sum
CREATE ROLE envsysfe PASSWORD 'md5c8ee62efe4cc0c54b05c1774c289ccf9' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
\c envsensor

-- Devices tables
CREATE TABLE device (
    id serial PRIMARY KEY,
    name character varying UNIQUE NOT NULL,
    version integer DEFAULT 1,
    active boolean DEFAULT true,
    floorplanPosition character varying DEFAULT NULL,
    muteAlarmsNotif boolean DEFAULT false,
    emailSender char,
    emailRecipients char, -- Comma sepaated string list of recipients
    lat real DEFAULT 0,
    long real DEFAULT 0,
    tempreatureWarning integer DEFAULT 320,
    tempreatureCritical integer DEFAULT 350,
    humidityWarning integer DEFAULT 700,
    humidityCritical integer DEFAULT 900
);
GRANT ALL ON device TO envsysfe;
GRANT ALL ON device_id_seq TO envsysfe;

-- Temperature and humidity log
CREATE TABLE temp_and_humd_log (
    id bigserial PRIMARY KEY,
    deletable boolean DEFAULT true, -- Mark as false on raise alarm
    tst timestamp without time zone DEFAULT now(),
    name character varying NOT NULL,
    ip inet NOT NULL,
    lat real DEFAULT 0,
    long real DEFAULT 0,
    sampletime timestamp without time zone NOT NULL,
    status integer DEFAULT 0,
    message character varying,
    temperature integer NOT NULL,
    humidity integer NOT NULL
);
GRANT SELECT,INSERT ON temp_and_humd_log TO envsysfe;
GRANT ALL ON temp_and_humd_log_id_seq TO envsysfe;
CREATE INDEX i01_temp_and_humd_log ON temp_and_humd_log (name,sampletime,status);

-- SMTP template
CREATE TABLE smtp_template (
  templateName varchar PRIMARY KEY,
  active boolean default true,
  smtpServerAddress inet DEFAULT '127.0.0.1',
  smtpServerPort integer DEFAULT 25,
  smtpAuth boolean DEFAULT false,
  smtpUser varchar,
  smtpPassword varchar
);
GRANT ALL ON smtp_template TO envsysfe;
INSERT INTO smtp_template(templateName) VALUES ('default');

-- User object
CREATE TABLE system_users (
  id serial PRIMARY KEY,
  singUptst timestamp DEFAULT now(),
  status integer DEFAULT 0, -- 0=active, 1=suspended
  userType integer NOT NULL, -- 0=system, 1=local login, 2=ldap login, 3=pam login, 4=TACACS login
  userNic varchar UNIQUE NOT NULL, -- base64 of only alphabetic and numeric characters
  userName varchar NOT NULL, -- base64 of any type of character
  userPassword varchar -- sha256sum password for local users
);
GRANT SELECT,INSERT,UPDATE ON system_users TO envsysfe;
GRANT USAGE ON system_users_id_seq TO envsysfe;
INSERT INTO system_users(id,userType,userNic,userName) VALUES (0,0,'system0','Web service front-end');

-- Alarm type. Based on RFC5674 (https://tools.ietf.org/html/rfc5674)
CREATE TABLE alarm_type (
  alarmNumber integer PRIMARY KEY,
  alarmSeverity varchar,
  alarmSeverityNumber integer,
  alarmResource varchar,
  autoClear boolean DEFAULT true,
  autoAck boolean DEFAULT false,
  alarmDescription varchar
);
GRANT SELECT ON alarm_type TO envsysfe;
INSERT INTO alarm_type(alarmNumber,alarmSeverityNumber,alarmSeverity,alarmResource,autoClear,alarmDescription) VALUES
(1,2,'Major','Environment temperature',true,'Temperature 1° threshold reached'),
(2,1,'Critical','Environment temperature',true,'Temperature 2° threshold reached'),
(3,2,'Major','Environment humidity',true,'Humidity 1° threshold reached'),
(4,1,'Critical','Environment humidity',true,'Humidity 2° threshold reached'),
(5,4,'Warning','Sensor',true,'Sensor not responding'),
(6,4,'Warning','Device',true,'Device not responding'),
(7,4,'Warning','Device',true,'Device reboot'),
(8,3,'Minor','Sensor',true,'Bad sensor data'),
(9,4,'Warning','O&M',false,'Configuration change'),
(10,5,'Notice','O&M',false,'User web login'),
(11,5,'Notice','O&M',false,'User web logout'),
(12,1,'Critical','System',true,'System database not available')
;

-- Alarm log
CREATE TABLE alarm_log (
  id bigserial PRIMARY KEY,
  raiseTst  timestamp DEFAULT now(),
  cleareTst timestamp,
  ackTst    timestamp,
  userId integer DEFAULT 0, -- 0=System
  status integer DEFAULT 0, -- 0-Active, 1-Cleared
  alarmNumber integer,
  temAndHumLogId bigint,
  ack boolean DEFAULT false
);
CREATE INDEX i01_alarm_log_tst         ON alarm_log(raiseTst);
CREATE INDEX i02_alarm_log_status      ON alarm_log(status);
CREATE INDEX i03_alarm_log_alarmNumber ON alarm_log(alarmNumber);
GRANT ALL ON alarm_log_id_seq TO envsysfe;
GRANT SELECT ON alarm_log TO envsysfe;
GRANT UPDATE (status,ack) ON alarm_log TO envsysfe;
