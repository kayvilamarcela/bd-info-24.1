import mysql.connector

connect = mysql.connector.connect(
    user= "myuser",
    password= "mypassword",
    host= "localhost",
    database= "mydatabase"
)

cursor = connect.cursor()

tabelas = ["TB_MATRICULA", "TB_ALUNO", "TB_PROFESSOR", "TB_DISCIPLINA"]

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS TB_ALUNO(
            id_aluno INT PRIMARY KEY,
            nomeAluno VARCHAR(50) NOT NULL
        );
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS TB_PROFESSOR(
            id_prof INT PRIMARY KEY,
            nomeProf VARCHAR(50) NOT NULL,
            disciplina VARCHAR(50) NOT NULL
        );
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS TB_DISCIPLINA(
            id_disc INT PRIMARY KEY,
            nomeDisc VARCHAR(50) NOT NULL,
            horas INT NOT NULL
        );
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS TB_MATRICULA(
            id_matricula INT PRIMARY KEY AUTO_INCREMENT,
            id_aluno INT,
            id_prof INT,
            id_disc INT,
            notaN1 DECIMAL(4,2),
            notaN2 DECIMAL(4,2),
            faltas INT,
            FOREIGN KEY (id_aluno) REFERENCES TB_ALUNO(id_aluno),
            FOREIGN KEY (id_prof) REFERENCES TB_PROFESSOR(id_prof),
            FOREIGN KEY (id_disc) REFERENCES TB_DISCIPLINA(id_disc)
        );
    """
)

connect.commit()

for item in range(len(tabelas)):
    cursor.execute(f"DELETE FROM {tabelas[item]};")
    cursor.execute(f"ALTER TABLE {tabelas[item]} AUTO_INCREMENT = 1;")
    connect.commit()

cursor.execute(
    """
        INSERT INTO TB_ALUNO(id_aluno, nomeAluno) 
        VALUES (1, "Marcela"), (2, "Nagyla"), (3, "Pedro")
        
    """
)

connect.commit()

cursor.execute(
    """
        INSERT INTO TB_PROFESSOR(id_prof, nomeProf, disciplina) 
        VALUES (1, "Prof kiara", "Matemática"), 
               (2, "Prof Ulisses", "Educação Fisica"), 
               (3, "Prof Hairon", " Prática Profissional")
        
    """
)

connect.commit()

cursor.execute(
    """
    INSERT INTO TB_DISCIPLINA(id_disc, nomeDisc, horas) 
    VALUES (1, "Matemática", 80),
           (2, "Educação Fisica", 60),
           (3, "Prática Profissional", 90);
    """
)

connect.commit()

cursor.execute(
    """
        INSERT INTO TB_MATRICULA(id_aluno, id_prof, id_disc, notaN1, notaN2, faltas) 
        VALUES (1, 1, 1, 8.0, 8.0, 5),
               (2, 2, 2, 6.0, 10.0, 12),
               (3, 3, 3, 6.0, 7.0, 3);
    """
)

connect.commit()

cursor.execute(
    """
        SELECT A.nomeAluno, M.notaN1, M.notaN2, M.faltas
        FROM TB_MATRICULA M
        JOIN TB_ALUNO A ON M.id_aluno = A.id_aluno;
    """
)

matriculas = cursor.fetchall()

for matricula in matriculas:
    nomeAluno, notaN1, notaN2, faltas = matricula
    if ((notaN1 + notaN2)/2) < 6:
        print(f"nome: {nomeAluno}, status: Reprovado por nota")
    elif faltas > 10:
        print(f"nome: {nomeAluno}, status: Reprovado por falta")
    else:
        print(f"nome: {nomeAluno}, status: Aprovado")


cursor.close()
connect.close()
