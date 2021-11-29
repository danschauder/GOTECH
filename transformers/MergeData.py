from sqlalchemy import create_engine

class MergeData():
    def __init__(self,verbose):
        self.verbose=verbose

    def update_table(self,schema,temp_table,dest_table,conn):
        table_exists_query = f"SELECT to_regclass('{schema}.{dest_table}');"
        rs = conn.execute(table_exists_query)
        table_exists = rs.fetchone()[0]
        if table_exists:
            conn.execute(f"""
            INSERT INTO {schema}.{dest_table}
            select
                c.*,
                ab2.*
            from 
                {temp_table} c
            cross join lateral 
                (select 
                    ogc_fid,
                    class_name,
                    area_sqkm,
                    wkb_geometry,
                    ab.wkb_geometry <#> c.geometry as dist
                from
                    staging.aca_benthic_4326 ab
                order by dist
                    limit 1
                ) ab2
            where
                ab2.dist<=0.5;
            """)
        else:
            conn.execute(f"""
            select INTO {schema}.{dest_table}
                c.*,
                ab2.*
            from 
                {temp_table} c
            cross join lateral 
                (select 
                    ogc_fid,
                    class_name,
                    area_sqkm,
                    wkb_geometry,
                    ab.wkb_geometry <#> c.geometry as dist
                from
                    staging.aca_benthic_4326 ab
                order by dist
                    limit 1
                ) ab2
            where
                ab2.dist<=0.5;
            """)
    
    def create_temp_table(self,temp_table,conn):
        conn.execute(f"""
        select * into temporary {temp_table} from raw.calipso
        limit 1;""")

        conn.execute(f'TRUNCATE TABLE {temp_table};')

    def get_calipso_months(self, conn):
        query="""
        select distinct 
        (cast("time_UTC" /100 as integer)) as calipso_month
        from raw.calipso
        order by calipso_month;
        """
        rs = conn.execute(query)
        return rs.fetchall()
    
    def add_calipso_to_temp(self,temp_table,month,conn):
        insert_query=f"""
        INSERT INTO {temp_table}
        SELECT * FROM raw.calipso
        WHERE (cast("time_UTC" /100 as integer)) = {month};
        """
        index_query="""CREATE INDEX 
                        calipso_geom_idx2 ON {temp_table}
                        USING GIST (geometry);"""
        conn.execute(insert_query)
        conn.execute(index_query)

    def merge(self):
        ## Create temp table
        ## Iterate through months
            ##populate temp table with month data
            ##create an index on the temp table
            ##Insert data into the final table
            ##truncate the temp table
            ##drop the index on the temp table
        TEMP_TABLE='calipso_temp'
        engine = create_engine('postgresql://{}@{}:{}/{}'.format("GOTECH", "127.0.0.1",5432, "coral_data"))
        with engine.connect() as conn:
            self.create_temp_table(TEMP_TABLE,conn)
            calipso_months = self.get_calipso_months(conn)
            for month_result in calipso_months:
                if self.verbose:
                    print(f'Inserting data for month {month}')
                month=month_result[0]
                self.add_calipso_to_temp(TEMP_TABLE,month,conn)
                self.update_table('models',TEMP_TABLE,'merged_full',conn)
                conn.execute(f'TRUNCATE TABLE {TEMP_TABLE};')
                conn.execute('DROP INDEX calipso_geom_idx2;')
            conn.close()
        
        