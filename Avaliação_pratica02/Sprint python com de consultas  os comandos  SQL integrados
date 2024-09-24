import mysql.connector
from mysql.connector import Error
import sys

def conectar():
    """Estabelece conexão com o banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Atualize se o host for diferente no Docker
            port=3306,
            user='myuser',           # Atualize conforme definido no docker-compose.yml
            password='mypassword',   # Atualize conforme definido no docker-compose.yml
            database='mydatabase'    # Certifique-se de que o banco de dados existe
        )
        if connection.is_connected():
            print("Conexão com o MySQL estabelecida com sucesso.")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        sys.exit(1)

def criar_tabelas(cursor):
    """Cria as tabelas necessárias no banco de dados."""
    script_sql = """
    CREATE TABLE IF NOT EXISTS TB_ALUNO (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        matricula VARCHAR(20) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS TB_DISCIPLINA (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        codigo VARCHAR(20) UNIQUE NOT NULL,
        carga_horaria INT NOT NULL CHECK (carga_horaria IN (20, 40, 80))
    );

    CREATE TABLE IF NOT EXISTS TB_PROFESSOR (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        departamento VARCHAR(100)
    );

    CREATE TABLE IF NOT EXISTS TB_MATRICULA (
        id INT AUTO_INCREMENT PRIMARY KEY,
        aluno_id INT NOT NULL,
        disciplina_id INT NOT NULL,
        professor_id INT NOT NULL,
        N1 DECIMAL(5,2) NOT NULL,
        N2 DECIMAL(5,2) NOT NULL,
        Faltas INT NOT NULL,
        FOREIGN KEY (aluno_id) REFERENCES TB_ALUNO(id) ON DELETE CASCADE,
        FOREIGN KEY (disciplina_id) REFERENCES TB_DISCIPLINA(id) ON DELETE CASCADE,
        FOREIGN KEY (professor_id) REFERENCES TB_PROFESSOR(id) ON DELETE CASCADE
    );
    """
    try:
        for result in cursor.execute(script_sql, multi=True):
            pass
        print("Tabelas criadas ou já existentes.")
    except Error as e:
        print(f"Erro ao criar tabelas: {e}")

def inserir_aluno(cursor):
    """Insere um novo aluno na tabela TB_ALUNO."""
    nome = input("Digite o nome do aluno: ").strip()
    matricula = input("Digite a matrícula do aluno: ").strip()
    try:
        query = "INSERT INTO TB_ALUNO (nome, matricula) VALUES (%s, %s)"
        cursor.execute(query, (nome, matricula))
        print("Aluno inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir aluno: {e}")

def inserir_disciplina(cursor):
    """Insere uma nova disciplina na tabela TB_DISCIPLINA com seleção de carga horária."""
    nome = input("Digite o nome da disciplina: ").strip()
    codigo = input("Digite o código da disciplina: ").strip()

    while True:
        try:
            print("\nSelecione a carga horária da disciplina:")
            print("1. 20 horas")
            print("2. 40 horas")
            print("3. 80 horas")
            escolha = input("Escolha uma opção (1-3): ").strip()
            if escolha == '1':
                carga_horaria = 20
                break
            elif escolha == '2':
                carga_horaria = 40
                break
            elif escolha == '3':
                carga_horaria = 80
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    try:
        query = "INSERT INTO TB_DISCIPLINA (nome, codigo, carga_horaria) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, codigo, carga_horaria))
        print("Disciplina inserida com sucesso.")
    except Error as e:
        print(f"Erro ao inserir disciplina: {e}")

def inserir_professor(cursor):
    """Insere um novo professor na tabela TB_PROFESSOR."""
    nome = input("Digite o nome do professor: ").strip()
    departamento = input("Digite o departamento do professor: ").strip()
    try:
        query = "INSERT INTO TB_PROFESSOR (nome, departamento) VALUES (%s, %s)"
        cursor.execute(query, (nome, departamento))
        print("Professor inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir professor: {e}")

def listar_alunos(cursor):
    """Lista todos os alunos."""
    try:
        query = "SELECT id, nome, matricula FROM TB_ALUNO"
        cursor.execute(query)
        alunos = cursor.fetchall()
        if alunos:
            print("\n--- Lista de Alunos ---")
            for aluno in alunos:
                print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Matrícula: {aluno[2]}")
        else:
            print("Nenhum aluno encontrado.")
    except Error as e:
        print(f"Erro ao listar alunos: {e}")

def listar_disciplinas(cursor):
    """Lista todas as disciplinas."""
    try:
        query = "SELECT id, nome, codigo, carga_horaria FROM TB_DISCIPLINA"
        cursor.execute(query)
        disciplinas = cursor.fetchall()
        if disciplinas:
            print("\n--- Lista de Disciplinas ---")
            for disciplina in disciplinas:
                print(f"ID: {disciplina[0]}, Nome: {disciplina[1]}, Código: {disciplina[2]}, Carga Horária: {disciplina[3]} horas")
        else:
            print("Nenhuma disciplina encontrada.")
    except Error as e:
        print(f"Erro ao listar disciplinas: {e}")

def listar_professores(cursor):
    """Lista todos os professores."""
    try:
        query = "SELECT id, nome, departamento FROM TB_PROFESSOR"
        cursor.execute(query)
        professores = cursor.fetchall()
        if professores:
            print("\n--- Lista de Professores ---")
            for professor in professores:
                print(f"ID: {professor[0]}, Nome: {professor[1]}, Departamento: {professor[2]}")
        else:
            print("Nenhum professor encontrado.")
    except Error as e:
        print(f"Erro ao listar professores: {e}")

def inserir_matricula(cursor, connection):
    """Insere uma nova matrícula na tabela TB_MATRICULA."""
    try:
        print("\nSelecione o Aluno:")
        listar_alunos(cursor)
        aluno_id = int(input("Digite o ID do aluno: ").strip())

        print("\nSelecione a Disciplina:")
        listar_disciplinas(cursor)
        disciplina_id = int(input("Digite o ID da disciplina: ").strip())

        print("\nSelecione o Professor:")
        listar_professores(cursor)
        professor_id = int(input("Digite o ID do professor: ").strip())

        N1 = float(input("Digite a nota N1: ").strip())
        N2 = float(input("Digite a nota N2: ").strip())
        faltas = int(input("Digite o número de faltas: ").strip())

        query = """
            INSERT INTO TB_MATRICULA (aluno_id, disciplina_id, professor_id, N1, N2, Faltas)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (aluno_id, disciplina_id, professor_id, N1, N2, faltas))
        connection.commit()
        print("Matrícula inserida com sucesso.")
    except Error as e:
        print(f"Erro ao inserir matrícula: {e}")
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos corretos.")

def calcular_media(N1, N2):
    """Calcula a média ponderada."""
    return ((N1 * 2) + (N2 * 3)) / 5

def determinar_status(media, faltas, carga_horaria):
    """Determina o status de aprovação considerando média e faltas."""
    limite_faltas = 0.25 * carga_horaria
    if media >= 6 and faltas <= limite_faltas:
        return "Aprovado"
    elif media < 6 and faltas <= limite_faltas:
        return "Reprovado por Média"
    elif media >= 6 and faltas > limite_faltas:
        return "Reprovado por Falta"
    else:
        return "Reprovado por Média e Falta"

def listar_status_aprovacao(cursor):
    """Lista o status de aprovação dos alunos matriculados."""
    try:
        query = """
            SELECT 
                a.nome AS Nome_Aluno,
                d.nome AS Nome_Disciplina,
                p.nome AS Nome_Professor,
                m.N1,
                m.N2,
                d.carga_horaria,
                m.Faltas
            FROM 
                TB_MATRICULA m
            JOIN TB_ALUNO a ON m.aluno_id = a.id
            JOIN TB_DISCIPLINA d ON m.disciplina_id = d.id
            JOIN TB_PROFESSOR p ON m.professor_id = p.id
        """
        cursor.execute(query)
        registros = cursor.fetchall()

        if not registros:
            print("Nenhuma matrícula encontrada.")
            return

        print("\n--- Status de Aprovação dos Alunos ---")
        for registro in registros:
            N1 = float(registro[3])
            N2 = float(registro[4])
            carga_horaria = registro[5]
            faltas = registro[6]
            media = calcular_media(N1, N2)
            status = determinar_status(media, faltas, carga_horaria)
            print(f"Aluno: {registro[0]}, Disciplina: {registro[1]}, Professor: {registro[2]}, N1: {N1}, N2: {N2}, Média: {media:.2f}, Faltas: {faltas}, Status: {status}")

    except Error as e:
        print(f"Erro ao listar status de aprovação: {e}")

def listar_alunos_reprovados(cursor):
    """Lista todos os alunos reprovados."""
    try:
        query = """
            SELECT 
                a.nome AS Nome_Aluno,
                d.nome AS Nome_Disciplina,
                p.nome AS Nome_Professor,
                m.N1,
                m.N2,
                d.carga_horaria,
                m.Faltas,
                CASE 
                    WHEN ((m.N1 * 2) + (m.N2 * 3)) / 5 < 6 AND m.Faltas > 0.25 * d.carga_horaria THEN 'Reprovado por Média e Falta'
                    WHEN ((m.N1 * 2) + (m.N2 * 3)) / 5 < 6 THEN 'Reprovado por Média'
                    WHEN m.Faltas > 0.25 * d.carga_horaria THEN 'Reprovado por Falta'
                END AS Status
            FROM 
                TB_MATRICULA m
            JOIN TB_ALUNO a ON m.aluno_id = a.id
            JOIN TB_DISCIPLINA d ON m.disciplina_id = d.id
            JOIN TB_PROFESSOR p ON m.professor_id = p.id
            WHERE 
                ((m.N1 * 2) + (m.N2 * 3)) / 5 < 6 
                OR m.Faltas > 0.25 * d.carga_horaria
        """
        cursor.execute(query)
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum aluno reprovado encontrado.")
            return

        print("\n--- Lista de Alunos Reprovados ---")
        for registro in registros:
            print(f"Aluno: {registro[0]}, Disciplina: {registro[1]}, Professor: {registro[2]}, N1: {registro[3]}, N2: {registro[4]}, Carga Horária: {registro[5]} horas, Faltas: {registro[6]}, Status: {registro[7]}")

    except Error as e:
        print(f"Erro ao listar alunos reprovados: {e}")

def listar_alunos_aprovados(cursor):
    """Lista todos os alunos aprovados."""
    try:
        query = """
            SELECT 
                a.nome AS Nome_Aluno,
                d.nome AS Nome_Disciplina,
                p.nome AS Nome_Professor,
                m.N1,
                m.N2,
                d.carga_horaria,
                m.Faltas
            FROM 
                TB_MATRICULA m
            JOIN TB_ALUNO a ON m.aluno_id = a.id
            JOIN TB_DISCIPLINA d ON m.disciplina_id = d.id
            JOIN TB_PROFESSOR p ON m.professor_id = p.id
            WHERE 
                ((m.N1 * 2) + (m.N2 * 3)) / 5 >= 6 
                AND m.Faltas <= 0.25 * d.carga_horaria
        """
        cursor.execute(query)
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum aluno aprovado encontrado.")
            return

        print("\n--- Lista de Alunos Aprovados ---")
        for registro in registros:
            N1 = float(registro[3])
            N2 = float(registro[4])
            media = calcular_media(N1, N2)
            print(f"Aluno: {registro[0]}, Disciplina: {registro[1]}, Professor: {registro[2]}, N1: {N1}, N2: {N2}, Média: {media:.2f}, Faltas: {registro[6]}, Status: Aprovado")

    except Error as e:
        print(f"Erro ao listar alunos aprovados: {e}")

def quantidade_alunos_aprovados(cursor):
    """Retorna a quantidade de alunos aprovados."""
    try:
        query = """
            SELECT COUNT(*) 
            FROM TB_MATRICULA m
            JOIN TB_DISCIPLINA d ON m.disciplina_id = d.id
            WHERE ((m.N1 * 2) + (m.N2 * 3)) / 5 >= 6 
                AND m.Faltas <= 0.25 * d.carga_horaria
        """
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"Quantidade de alunos aprovados: {count}")
    except Error as e:
        print(f"Erro ao contar alunos aprovados: {e}")

def quantidade_alunos_reprovados(cursor):
    """Retorna a quantidade de alunos reprovados."""
    try:
        query = """
            SELECT COUNT(*) 
            FROM TB_MATRICULA m
            JOIN TB_DISCIPLINA d ON m.disciplina_id = d.id
            WHERE ((m.N1 * 2) + (m.N2 * 3)) / 5 < 6 
                OR m.Faltas > 0.25 * d.carga_horaria
        """
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"Quantidade de alunos reprovados: {count}")
    except Error as e:
        print(f"Erro ao contar alunos reprovados: {e}")

def main():
    """Função principal para gerenciar o fluxo do programa."""
    connection = conectar()
    cursor = connection.cursor()

    criar_tabelas(cursor)

    while True:
        print("\n--- Sistema Acadêmico ---")
        print("1. Inserir Aluno")
        print("2. Inserir Disciplina")
        print("3. Inserir Professor")
        print("4. Inserir Matrícula")
        print("5. Listar Alunos")
        print("6. Listar Disciplinas")
        print("7. Listar Professores")
        print("8. Listar Status de Aprovação")
        print("9. Listar Alunos Reprovados")
        print("10. Listar Alunos Aprovados")
        print("11. Quantidade de Alunos Aprovados")
        print("12. Quantidade de Alunos Reprovados")
        print("13. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            inserir_aluno(cursor)
        elif opcao == '2':
            inserir_disciplina(cursor)
        elif opcao == '3':
            inserir_professor(cursor)
        elif opcao == '4':
            inserir_matricula(cursor, connection)
        elif opcao == '5':
            listar_alunos(cursor)
        elif opcao == '6':
            listar_disciplinas(cursor)
        elif opcao == '7':
            listar_professores(cursor)
        elif opcao == '8':
            listar_status_aprovacao(cursor)
        elif opcao == '9':
            listar_alunos_reprovados(cursor)
        elif opcao == '10':
            listar_alunos_aprovados(cursor)
        elif opcao == '11':
            quantidade_alunos_aprovados(cursor)
        elif opcao == '12':
            quantidade_alunos_reprovados(cursor)
        elif opcao == '13':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

    cursor.close()
    connection.close()

# Chamada direta da função main()
main()
