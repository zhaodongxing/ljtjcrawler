#带看情况统计
select date,sum(recentvisit) from regions.mj group by date order by date;
select date,sum(recentvisit) from regions.tyc group by date order by date;
#房源数统计
select date,sum(id) from regions.mj group by date order by date;
select date,sum(id) from regions.tyc group by date order by date;
#成交房源
select count(*) from regions.tyc where date='20161222' and id not in (select id from regions.tyc where date='20161223');
select count(*) from regions.mj where date='20161222' and id not in (select id from regions.mj where date='20161223');
#新上房源
select count(*) from regions.tyc where date='20161223' and id not in (select id from regions.tyc where date='20161222');
select count(*) from regions.mj where date='20161223' and id not in (select id from regions.mj where date='20161222');
#均价
select avg(price) from regions.tyc housetype <> '商住两用'  group by date; 
select avg(price) from regions.mj housetype <> '商住两用' group by date;

