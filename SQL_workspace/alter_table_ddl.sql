# ALTER TABLE语句用于添加、删除或修改现有表中的列。

# ALTER TABLE语句还用于在现有表上添加和删除各种约束。

-- 对于表格fact_booksales，在名为 sales_book 的约束中，设置book_id为外键
ALTER TABLE fact_booksales ADD CONSTRAINT sales_book
    FOREIGN KEY (book_id) REFERENCES dim_book_star(book_id);
    
-- Add the time_id foreign key
ALTER TABLE fact_booksales ADD CONSTRAINT sales_time
    FOREIGN KEY (time_id) REFERENCES dim_time_star (time_id);
    
-- Add the store_id foreign key
ALTER TABLE fact_booksales ADD CONSTRAINT sales_store
    FOREIGN KEY (store_id) REFERENCES dim_store_star (store_id); 
    
