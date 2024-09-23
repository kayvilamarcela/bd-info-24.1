import mysql.connector

# Função para calcular status de aprovação
def calcular_status(n1, n2, faltas):
    media = (n1 + n2) / 2
    if faltas > 10:
        return "Reprovado por Faltas"
    elif media >= 6.0:
        return "Aprovado"
    else:
        return "Reprovado por Nota"

# Conectar ao servidor MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword"
)

cursor = conexao.cursor()

# Criar o banco de dados 'mydatabase'
cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase;")
cursor.execute("USE mydatabase;")

# Criar as tabelas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TB_ALUNO (
        id_aluno INT PRIMARY KEY AUTO_INCREMENT,
        nome_aluno VARCHAR(100) NOT NULL,
        data_nascimento DATE NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TB_PROFESSOR (
        id_professor INT PRIMARY KEY AUTO_INCREMENT,
        nome_professor VARCHAR(100) NOT NULL,
        especialidade VARCHAR(100)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TB_DISCIPLINA (
        id_disciplina INT PRIMARY KEY AUTO_INCREMENT,
        nome_disciplina VARCHAR(100) NOT NULL,
        carga_horaria INT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TB_MATRICULA (
        id_matricula INT PRIMARY KEY AUTO_INCREMENT,
        id_aluno INT UNIQUE,
        id_professor INT,
        id_disciplina INT,
        nota_n1 DECIMAL(5, 2),
        nota_n2 DECIMAL(5, 2),
        faltas INT,
        FOREIGN KEY (id_aluno) REFERENCES TB_ALUNO(id_aluno),
        FOREIGN KEY (id_professor) REFERENCES TB_PROFESSOR(id_professor),
        FOREIGN KEY (id_disciplina) REFERENCES TB_DISCIPLINA(id_disciplina)
    );
""")

# Alimentar as tabelas com dados de exemplo
cursor.execute("""
    INSERT INTO TB_ALUNO (nome_aluno, data_nascimento)
    VALUES ('Paulo Santos', '2000-05-10'),
           ('Ana Lemos', '1998-12-15'),
           ('Carlos Mendes', '1999-07-20'),
           ('Maria Ribeiro', '2001-02-25')
    ON DUPLICATE KEY UPDATE nome_aluno=VALUES(nome_aluno);
""")

cursor.execute("""
    INSERT INTO TB_PROFESSOR (nome_professor, especialidade)
    VALUES ('Prof. Beatriz', 'Matemática'),
           ('Prof. João', 'História'),
           ('Prof. Cláudio', 'Física')
    ON DUPLICATE KEY UPDATE nome_professor=VALUES(nome_professor);
""")

cursor.execute("""
    INSERT INTO TB_DISCIPLINA (nome_disciplina, carga_horaria)
    VALUES ('Matemática', 60),
           ('História', 40),
           ('Física', 50)
    ON DUPLICATE KEY UPDATE nome_disciplina=VALUES(nome_disciplina);
""")

# Exemplo de matrículas com aprovações e reprovações
cursor.execute("""
    INSERT INTO TB_MATRICULA (id_aluno, id_professor, id_disciplina, nota_n1, nota_n2, faltas)
    VALUES (1, 1, 1, 7.5, 8.0, 2),  -- Aprovado
           (2, 2, 2, 6.0, 6.5, 4),  -- Aprovado
           (3, 3, 3, 5.0, 4.5, 12),  -- Reprovado por faltas
           (4, 1, 1, 4.0, 5.0, 6)   -- Reprovado por nota
    ON DUPLICATE KEY UPDATE nota_n1=VALUES(nota_n1), nota_n2=VALUES(nota_n2), faltas=VALUES(faltas);
""")

conexao.commit()

# Consulta 1: Listar alunos reprovados
cursor.execute("""
    SELECT A.nome_aluno, D.nome_disciplina, P.nome_professor, M.nota_n1, M.nota_n2,
           (M.nota_n1 + M.nota_n2) / 2 AS media, M.faltas,
           CASE
               WHEN M.faltas > 10 THEN 'Reprovado por Faltas'
               WHEN (M.nota_n1 + M.nota_n2) / 2 < 6 THEN 'Reprovado por Nota'
               ELSE 'Aprovado'
           END AS status_reprovacao
    FROM TB_MATRICULA M
    JOIN TB_ALUNO A ON M.id_aluno = A.id_aluno
    JOIN TB_DISCIPLINA D ON M.id_disciplina = D.id_disciplina
    JOIN TB_PROFESSOR P ON M.id_professor = P.id_professor
    WHERE M.faltas > 10 OR (M.nota_n1 + M.nota_n2) / 2 < 6;
""")
alunos_reprovados = cursor.fetchall()

print("Alunos Reprovados:")
for aluno in alunos_reprovados:
    print(aluno)

# Consulta 2: Listar alunos aprovados
cursor.execute("""
    SELECT A.nome_aluno, D.nome_disciplina, P.nome_professor, M.nota_n1, M.nota_n2,
           (M.nota_n1 + M.nota_n2) / 2 AS media, M.faltas,
           'Aprovado por Média' AS status_aprovacao
    FROM TB_MATRICULA M
    JOIN TB_ALUNO A ON M.id_aluno = A.id_aluno
    JOIN TB_DISCIPLINA D ON M.id_disciplina = D.id_disciplina
    JOIN TB_PROFESSOR P ON M.id_professor = P.id_professor
    WHERE M.faltas <= 10 AND (M.nota_n1 + M.nota_n2) / 2 >= 6;
""")
alunos_aprovados = cursor.fetchall()

print("\nAlunos Aprovados:")
for aluno in alunos_aprovados:
    print(aluno)

# Consulta 3: Quantidade de alunos aprovados
cursor.execute("""
    SELECT COUNT(*) AS total_aprovados
    FROM TB_MATRICULA M
    WHERE M.faltas <= 10 AND (M.nota_n1 + M.nota_n2) / 2 >= 6;
""")
qtd_aprovados = cursor.fetchone()

print(f"\nQuantidade de Alunos Aprovados: {qtd_aprovados[0]}")

# Consulta 4: Quantidade de alunos reprovados
cursor.execute("""
    SELECT COUNT(*) AS total_reprovados
    FROM TB_MATRICULA M
    WHERE M.faltas > 10 OR (M.nota_n1 + M.nota_n2) / 2 < 6;
""")
qtd_reprovados = cursor.fetchone()

print(f"Quantidade de Alunos Reprovados: {qtd_reprovados[0]}")

# Fechar a conexão
cursor.close()
conexao.close()

print("\nConsultas realizadas com sucesso.")
