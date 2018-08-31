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
    lat real DEFAULT 0,
    long real DEFAULT 0,
    sampletime timestamp without time zone NOT NULL,
    status integer DEFAULT 0,
    message character varying,
    temperature integer NOT NULL,
    humidity integer NOT NULL
);
GRANT ALL ON temp_and_humd_log TO envsysfe;
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

-- Alarm type
CREATE TABLE alarm_type (
  alarmNumber integer PRIMARY KEY,
  alarmSeverity varchar,
  autoAck boolean default false,
  alarmDescription varchar
);
GRANT ALL ON alarm_type TO envsysfe;
INSERT INTO alarm_type(alarmNumber,alarmSeverity,autoAck,alarmDescription) VALUES
(1,'warning',true,'Temperature warning threshold reached'),
(2,'critical',true,'Temperature critical threshold reached'),
(3,'warning',true,'Humidity warning threshold reached'),
(4,'critical',true,'Humidity critical threshold reached'),
(5,'critical',true,'Sensor not responding'),
(6,'critical',true,'Device not responding')
;

-- Alarm log
CREATE TABLE alarm_log (
  id bigserial PRIMARY KEY,
  alarmNumber integer,
  temAndHumLogId bigint,
  ack boolean DEFAULT false
);
GRANT ALL ON alarm_log_id_seq TO envsysfe;
GRANT ALL ON alarm_log TO envsysfe;
