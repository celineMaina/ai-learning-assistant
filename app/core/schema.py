import asyncio
from app.core.db_connection import connect

async def create_schema():
    conn = await connect()

    await conn.execute("""
        CREATE SCHEMA IF NOT EXISTS dsa_course;
    """
    )
    print("Schema 'dsa_course' created.")

    # Student table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.students (
                       student_id VARCHAR(10) PRIMARY KEY,
                       first_name VARCHAR(50),
                       last_name VARCHAR(50),
                       email VARCHAR(50),
                       date_enrolled DATE,
                       cohort INT,
                       status VARCHAR(50) 
                       );
    """
    )
    print("Table 'students' created.")

    # Trainers table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.trainers (
                       trainer_id VARCHAR(10) PRIMARY KEY,
                       first_name VARCHAR(50),
                       last_name VARCHAR(50),
                       email VARCHAR(50),
                       specialization VARCHAR(100)
                       );
    """
    )
    print("Table 'trainers' created.")

    # Subjects table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.subjects (
                       subject_id VARCHAR(10) PRIMARY KEY,
                       name VARCHAR(200),
                       description VARCHAR(300)
                       );
    """
    )
    print("Table 'subjects' created.")

    # Trainers and subjects linking table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.trainer_subjects(
                       trainer_id VARCHAR(10) REFERENCES dsa_course.trainers(trainer_id),
                       subject_id VARCHAR(10) REFERENCES dsa_course.subjects(subject_id),
                       PRIMARY KEY (trainer_id, subject_id)
                       );
    """
    )

    # Quiz results table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.assessments (
                       quiz_id VARCHAR(10) PRIMARY KEY,
                       subject_id VARCHAR(10) REFERENCES dsa_course.subjects(subject_id),
                       title VARCHAR(100)
                       );
    """
    )
    print("Table 'assessments' created.")

    #Performance table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_course.performance (
                       performance_id SERIAL PRIMARY KEY,
                       subject_id VARCHAR(10) REFERENCES dsa_course.subjects(subject_id),
                       student_id VARCHAR(10) REFERENCES dsa_course.students(student_id),
                       avg_quiz_score FLOAT,
                       avg_project_score FLOAT,
                       final_project_score FLOAT
                       );
    """
    )
    print("Table 'performance' created.")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(create_schema())