import asyncio
from app.core.db_connection import connect

async def seed_db():
    conn = await connect()

    await conn.execute("""
        INSERT INTO dsa_course.students (student_id, first_name, last_name, email, date_enrolled, cohort, status)
        VALUES
        ('S0101', 'Sheila', 'Njeri', 'sheilanjeri@gmail.com', '2025-09-15', 4, 'active'),
        ('S0102', 'Brian', 'Otieno', 'brian.otieno@gmail.com', '2025-09-15', 4, 'active'),
        ('S0103', 'Faith', 'Nanjala', 'faithwanjiku@gmail.com', '2025-09-15', 4, 'active'),
        ('S0104', 'Daudi', 'Juma', 'davidmwangi@gmail.com', '2025-09-15', 4, 'active');
    """
    )

    await conn.execute("""
        INSERT INTO dsa_course.trainers (trainer_id, first_name, last_name, email, specialization)
        VALUES
        ('T001', 'James', 'Kariuki', 'james.kariuki@gmail.com', 'Excel & Power BI'),
        ('T002', 'Amina', 'Hassan', 'amina.hassan@gmail.com', 'SQL & Databases'),
        ('T003', 'Peter', 'Kamau', 'peter.kamau@gmail.com', 'Python & Machine Learning'),
        ('T004', 'Grace', 'Naliaka', 'grace.naliaka@gmail.com', 'Statistics & AI Engineering');
    """
    )

    await conn.execute("""
        INSERT INTO dsa_course.subjects (subject_id, name, description)
        VALUES
        ('SUB01', 'Excel', 'Spreadsheet analysis and data preparation'),
        ('SUB02', 'Power BI', 'Data visualization and dashboards'),
        ('SUB03', 'SQL', 'Relational databases and querying'),
        ('SUB04', 'Python', 'Python programming for data analysis'),
        ('SUB05', 'Machine Learning & Deep Learning', 'Predictive modeling and neural networks'),
        ('SUB06', 'Statistics', 'Statistical reasoning and hypothesis testing'),
        ('SUB07', 'AI Engineering', 'Building and deploying AI systems');
    """
    )

    await conn.execute("""
        INSERT INTO dsa_course.trainer_subjects (trainer_id, subject_id)
        VALUES
        ('T001', 'SUB01'),  -- Excel
        ('T001', 'SUB02'),  -- Power BI
        ('T002', 'SUB03'),  -- SQL
        ('T003', 'SUB04'),  -- Python
        ('T003', 'SUB05'),  -- Machine Learning
        ('T004', 'SUB06'),  -- Statistics
        ('T004', 'SUB07');  -- AI Engineering
    """
    )

    await conn.execute("""
        INSERT INTO dsa_course.assessments (quiz_id, subject_id, title)
        VALUES
        ('Q001', 'SUB01', 'Excel Basics Quiz'),
        ('Q002', 'SUB02', 'Power BI Dashboard Quiz'),
        ('Q003', 'SUB03', 'SQL Joins Assessment'),
        ('Q004', 'SUB04', 'Python Data Structures Quiz'),
        ('Q005', 'SUB05', 'Machine Learning Fundamentals'),
        ('Q006', 'SUB06', 'Statistics Concepts Quiz'),
        ('Q007', 'SUB07', 'AI Systems Design Quiz');
    """
    )

    await conn.execute("""
        INSERT INTO dsa_course.performance (student_id, student_id, avg_quiz_score, avg_project_score, final_project_score)
        VALUES
        ('SUB01', 'S0101', 85, 88, 90),
        ('SUB02', 'S0101', 80, 84, 87),
        ('SUB03', 'S0102', 78, 82, 85),
        ('SUB04', 'S0102', 88, 90, 92),
        ('SUB05', 'S0103', 75, 79, 83),
        ('SUB06', 'S0103', 82, 85, 88),
        ('SUB07', 'S0104', 90, 92, 95);
    """
    )

    print('Sample data inserted.')

    await conn.close()

if __name__ == "__main__":
    asyncio.run(seed_db())