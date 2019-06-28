-- Emily Van Laarhoven and Marissa Okoli
-- SQL DDL for final project, OddJobs
-- Last edited: 4/19/17, Evanlaar

-- using account oddjobs@cs.wellesley.edu
use oddjobs_db;

-- drop tables if they already exist
drop table if exists rating;
drop table if exists job;
drop table if exists account;

-- account table contains id, name, rating, and address for both employers and employees
create table account (
       uid integer auto_increment primary key,
       nm varchar(50) not null,
       rating_avg integer not null,
       street varchar(50),
       town varchar(50),
       st char(2),
       skills SET('yardwork','carpentry','tutoring','childcare'),
       pic varchar(50),
       active tinyint not null default 1,-- 1 is active, 0 is not
       pwd char(64) not null,
       salt char(32) CHARACTER SET utf8mb4 not null, -- character set for os.urandom salt values
       email varchar(50) not null
) ENGINE=InnoDB;

-- job table contains all job postings
create table job (
       jid integer auto_increment primary key,
       title varchar(50) not null,
       description varchar(1000),
       location varchar(5), --zip code?
       dt date,
       pay integer,
       poster integer,
       INDEX(poster),
       foreign key (poster) references account(uid) on delete cascade, 
       	       -- delete cascade : if uid deleted, all jobs deleted too 
       skills_required SET('yardwork','carpentry','tutoring','childcare'), -- may opt to make this dropdown with enum
       available tinyint -- 1 is available, 0 is unavailable
) ENGINE = InnoDB;

-- rating table contains all single ratings given after a job is completed
create table rating (
       jid integer,
       INDEX (jid),
       foreign key (jid) references job(jid) on delete cascade,
      	       -- want to keep rating but dont need uid if parent deleted?
       employee_id integer,
       INDEX (employee_id),
       foreign key (employee_id) references account(uid) on delete cascade,
       employer_id integer,
       INDEX (employer_id),
       foreign key (employer_id) references account(uid) on delete cascade,
       employee_rating integer,
       employer_rating integer,
       employee_review varchar(1000),
       employer_review varchar(1000)
) ENGINE=InnoDB;       