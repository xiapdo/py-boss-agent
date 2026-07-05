"""
初始化面试模块 MySQL 数据库表
用法: py interview/init_db.py

环境变量:
  MYSQL_HOST      - MySQL 主机地址 (默认 127.0.0.1)
  MYSQL_PORT      - MySQL 端口 (默认 3306)
  MYSQL_USER      - MySQL 用户名 (默认 root)
  MYSQL_PASSWORD  - MySQL 密码 (必填)
"""
import os
import pymysql

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "charset": "utf8mb4",
}

# Step 1: 建库
conn = pymysql.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute(
    "CREATE DATABASE IF NOT EXISTS ai_jobs_db "
    "DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci"
)
conn.commit()
cur.close()
conn.close()
print("[OK] database ai_jobs_db")

# Step 2: 建表
DB_CONFIG["database"] = "ai_jobs_db"
conn = pymysql.connect(**DB_CONFIG)
cur = conn.cursor()

# 2.1 interview_records —— 面试记录
cur.execute("""
    CREATE TABLE IF NOT EXISTS interview_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(32) NOT NULL,
        question_id INT,
        question TEXT,
        user_answer TEXT,
        score FLOAT,
        feedback TEXT,
        category VARCHAR(64) DEFAULT '',
        job_focus TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_session (session_id),
        INDEX idx_category (category),
        INDEX idx_score (score)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")
print("[OK] interview_records")

# 2.2 interview_qa_pairs —— 面试题库 + embedding
cur.execute("""
    CREATE TABLE IF NOT EXISTS interview_qa_pairs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(64) NOT NULL DEFAULT '',
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        difficulty VARCHAR(16) DEFAULT 'medium',
        embedding LONGTEXT,
        related_skills VARCHAR(256) DEFAULT '',
        source_job_id INT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FULLTEXT INDEX ft_question (question)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")
print("[OK] interview_qa_pairs")

# 2.3 job_requirements —— 岗位 JD
cur.execute("""
    CREATE TABLE IF NOT EXISTS job_requirements (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(128) NOT NULL DEFAULT '',
        salary VARCHAR(64) DEFAULT '',
        company VARCHAR(128) DEFAULT '',
        experience VARCHAR(32) DEFAULT '',
        education VARCHAR(32) DEFAULT '',
        requirement_category VARCHAR(64) DEFAULT '',
        requirement_text TEXT,
        source_url VARCHAR(512) DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")
print("[OK] job_requirements")

conn.commit()
cur.close()
conn.close()
print("\nDone - all 3 tables ready.")
