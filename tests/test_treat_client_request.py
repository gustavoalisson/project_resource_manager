from ..process_purchase import check_product_existence, check_sufficient_quantity

import pytest

# Mockando exemplo de teste
@pytest.fixture
def sample_stock():
    return {
        'Produto': ['Cadeira Gamer', 'Teclado Gamer', 'Mouse Gamer'],
        'Quantidade': [10, 20, 30]
    }

# Mockando um exemplo de logger     
@pytest.fixture
def sample_logger():
    class LoggerMock:
        def __init__(self):
            self.warnings = []
            self.infos = []

        def warning(self, message):
            self.warnings.append(message)

        def info(self, message):
            self.infos.append(message)

    return LoggerMock()    


def test_check_product_existence(sample_stock, sample_logger):
    assert check_product_existence(sample_stock, 'Cadeira Gamer', sample_logger) == True
    assert check_product_existence(sample_stock, 'Cadeira Gamer Azul Dragon', sample_logger) == False
    
    assert len(sample_logger.warnings) == 1

def test_check_sufficient_quantity(sample_stock, sample_logger):
    assert check_sufficient_quantity(sample_stock, 'Cadeira Gamer', 5, sample_logger) == True
    assert check_sufficient_quantity(sample_stock, 'Cadeira Gamer', 95, sample_logger) == False
    assert len(sample_logger.warnings) == 1  
    
    