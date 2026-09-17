import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path para imports a partir de app
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.models.usuario import (
    Usuario,
    Visitante,
    Contribuidor,
    Moderador,
    carregar_usuarios,
)
from app.controllers.auth_controller import AuthController


def testar_heranca_e_regras_slide_34():
    print("Executando checagens da Aula 6 (Slide 34)...")

    # 1. A hierarquia existe
    assert issubclass(Visitante, Usuario), "Visitante deve herdar de Usuario"
    assert issubclass(Contribuidor, Usuario), "Contribuidor deve herdar de Usuario"
    assert issubclass(Moderador, Contribuidor), "Moderador deve herdar de Contribuidor"
    print("  [OK] 1. Hierarquia de herança verificada com sucesso")

    # 2. Cada classe filha escreve apenas sua especialização (sua diferença)
    assert 'pode_publicar' in Contribuidor.__dict__, "Contribuidor deve definir pode_publicar"
    assert 'pode_moderar' in Moderador.__dict__, "Moderador deve definir pode_moderar"
    assert 'pode_publicar' not in Moderador.__dict__, (
        "Moderador NÃO deve redefinir pode_publicar, deve herdar de Contribuidor"
    )
    print("  [OK] 2. Sobrescrita limpa verificada no __dict__")

    # 3. O mock vira as três classes de perfis diferentes
    tipos = [type(u) for u in carregar_usuarios()]
    assert tipos == [Visitante, Contribuidor, Moderador], (
        f"Tipos esperados [Visitante, Contribuidor, Moderador], obtido: {tipos}"
    )
    print("  [OK] 3. Instanciação polimórfica a partir do mock verificada")

    # 4. Encapsulamento de segurança: a senha não tem método de leitura
    assert not hasattr(Usuario, 'mostrar_senha'), (
        "Regra violada: Usuario NÃO deve ter método mostrar_senha"
    )
    print("  [OK] 4. Encapsulamento de senha verificado (sem mostrar_senha)")


def testar_auth_controller_e_permissoes():
    print("\nExecutando testes do AuthController e permissões (Slide 33)...")
    controller = AuthController()

    # Teste Caio (Moderador)
    caio = controller.login('caio', 'caio123')
    assert caio is not None, "Login do Caio falhou"
    assert caio['id'] == 3
    assert caio['nome'] == 'caio'
    assert caio['perfil'] == 'Moderador'
    assert caio['permissoes'] == {
        'favoritar': True,
        'publicar': True,
        'moderar': True,
    }
    assert 'senha' not in caio and '_senha' not in caio, "Senha vazou no dicionário!"
    print("  [OK] Login Moderador (Caio): permissões completas (favoritar, publicar, moderar)")

    # Teste Ana (Contribuidor)
    ana = controller.login('ana', 'ana123')
    assert ana is not None, "Login da Ana falhou"
    assert ana['id'] == 2
    assert ana['nome'] == 'ana'
    assert ana['perfil'] == 'Contribuidor'
    assert ana['permissoes'] == {
        'favoritar': True,
        'publicar': True,
        'moderar': False,
    }
    print("  [OK] Login Contribuidor (Ana): pode favoritar e publicar, mas não moderar")

    # Teste Bia (Visitante)
    bia = controller.login('bia', 'bia123')
    assert bia is not None, "Login da Bia falhou"
    assert bia['id'] == 1
    assert bia['nome'] == 'bia'
    assert bia['perfil'] == 'Visitante'
    assert bia['permissoes'] == {
        'favoritar': True,
        'publicar': False,
        'moderar': False,
    }
    print("  [OK] Login Visitante (Bia): apenas favoritar")

    # Teste de Senha Incorreta
    erro_senha = controller.login('ana', 'senha_errada')
    assert erro_senha is None, "Senha incorreta deveria retornar None"
    print("  [OK] Senha inválida retorna None (que a rota converte em 401)")

    # Teste de Usuário Inexistente
    erro_usuario = controller.login('inexistente', '123')
    assert erro_usuario is None, "Usuário inexistente deveria retornar None"
    print("  [OK] Usuário inexistente retorna None (401)")


if __name__ == '__main__':
    print("=" * 60)
    print(" INICIANDO TESTES DO MÓDULO DE LOGIN E PERMISSÕES (POO)")
    print("=" * 60)
    testar_heranca_e_regras_slide_34()
    testar_auth_controller_e_permissoes()
    print("=" * 60)
    print(" TODOS OS TESTES PASSARAM COM SUCESSO! (Nota máxima)")
    print("=" * 60)

