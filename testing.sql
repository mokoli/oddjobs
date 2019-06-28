-- Emily Van Laarhoven
-- file for testing sql ddl for OddJobs 

use oddjobs_db;

insert into account values (1,"Emily Van Laarhoven",5,"4 Tara Rd","Southborough","MA","carpentry",null,1);
insert into account values (2, "Marissa Okoli",4,"1 Main St","Wellesley","MA","tutoring",null,1);

insert into job values (1,"Raking Leaves","Come rake leaves","Wellesley College","2017-05-01",10,1,"raking",1);
insert into job values (2,"Math tutor","Need calc tutor","Science Center","2017-04-19",15,2,"math",1);
insert into job values (3,"Editor","Need someone to edit my cover letter","PLTC","2017-04-25",12,2,"writing",1);

insert into rating values (1,2,1,5,4,"employee is cool","employer is ok");
insert into rating values (2,1,2,4,5,"employee was good","great to work for");
insert into rating values (3,1,2,3,3,"she was late","she was fine");