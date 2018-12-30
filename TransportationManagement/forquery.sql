show tables ;

show tables;

select * from Car;
select * from auth_group;
select * from auth_user;
select * from auth_user_groups;
select * from accident;
select * from proposer;
select * from driver;
select * from record;

describe Car;
describe Driver;
describe Record;
describe Proposer;
describe Accident;

show full columns in Proposer;
show full columns in Record;
show full columns in Car;
show full columns in Driver;
show full columns in Accident;


show tables;
show full columns from proposer;



insert into car (CNo, CType, COilConsumpution, isAvailable)
values ('豫B1003', '小型车', 300, 1 );
insert into car (CNo, CType, COilConsumpution, isAvailable)
values ('鲁N5203', '小型车', 300, 1 );

insert into driver (DName, DSex, DAge, PhoneNum, Hiredata, isAvailable)
values ('Marcy', 1, 40, 15782930382, now(), 1);

insert into proposer (CType, Num, Mileage, Date, isRecived)
values ('鲁N5203', 100, 1000, now(), 0);

insert into record (STime, ETime, OilConsumpution, isDelete, CNo_id, DName, DNo_id)
values (now(), '2019-03-04', 49000, 0, '鲁N5203', 'Marcy', 1);

insert into accident (SGCNo, Time, Spot, Cause, Money, isDelete, ZSCNo_id, ZSDName, ZSDNo_id)
values ('鲁N5204', now(), '市中心', '不详', 3000, false, '鲁N5203', 'Marcy', 1);

