import unittest
import os
import shutil
import zipfile
from pathlib import Path
from script import create_directory_structure, move_articles_to_category, convert_html_to_markdown, sanitize_markdown_files, main

class TestDoc360Migration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar um ambiente de teste com diretórios temporários
        cls.test_dir = Path("test_output")
        cls.test_dir.mkdir(exist_ok=True)
        
        # Criar diretório de origem e arquivos de teste
        cls.source_dir = cls.test_dir / "source"
        cls.source_dir.mkdir(exist_ok=True)
        
        # Criar exemplo de arquivos HTML e Markdown para conversão e sanitização
        with open(cls.source_dir / "test_article.html", "w") as f:
            f.write('<h1>Title</h1><p>Content with <a href="#">link</a>.</p>')
        
        with open(cls.source_dir / "test_markdown.md", "w") as f:
            f.write('# Title\n\n**Texto em negrito** e _texto em itálico_.')
        
        # Simular o arquivo ZIP contendo a estrutura esperada
        cls.zip_path = cls.test_dir / "document360_export.zip"
        with zipfile.ZipFile(cls.zip_path, 'w') as zipf:
            zipf.write(cls.source_dir / "test_article.html", arcname="v3.33/articles/test_article.html")
            zipf.write(cls.source_dir / "test_markdown.md", arcname="v3.33/articles/test_markdown.md")
            zipf.writestr("v3.33/v3-33_categories_articles.json", '{"Categories": [{"Title": "Test Category", "Articles": [{"Path": "test_article.html"}]}]}')

    @classmethod
    def tearDownClass(cls):
        # Limpar o ambiente de teste
        shutil.rmtree(cls.test_dir)

    def test_directory_structure_creation(self):
        """Testar se a estrutura de diretórios é criada corretamente a partir do JSON."""
        create_directory_structure(str(self.test_dir), [{'Title': 'Test Category', 'Articles': []}])
        self.assertTrue((self.test_dir / "Test Category").exists(), "A pasta da categoria não foi criada corretamente.")

    def test_move_articles(self):
        """Testar se os artigos são movidos corretamente para suas respectivas categorias."""
        category_path = self.test_dir / "Test Category"
        article = {'Path': 'test_article.html'}
        move_articles_to_category(str(category_path), [article])
        self.assertTrue((category_path / 'test_article.html').exists(), "O artigo não foi movido para a categoria correta.")

    def test_convert_html_to_markdown(self):
        """Testar a conversão de HTML para Markdown."""
        convert_html_to_markdown(str(self.source_dir))
        md_file_path = self.source_dir / "test_article.md"
        self.assertTrue(md_file_path.exists(), "O arquivo HTML não foi convertido para Markdown.")
        with open(md_file_path, 'r') as f:
            content = f.read()
        self.assertIn("# Title", content, "O título não foi convertido corretamente.")

    def test_sanitize_markdown(self):
        """Testar a sanitização do Markdown."""
        sanitize_markdown_files(str(self.source_dir))
        md_file_path = self.source_dir / "test_markdown.md"
        with open(md_file_path, 'r') as f:
            content = f.read()
        self.assertNotIn("**", content, "A sanitização do Markdown não removeu formatação problemática.")
        self.assertNotIn("_", content, "A sanitização do Markdown não removeu itálico problemático.")

    def test_main_function(self):
        """Testar o fluxo principal de migração, incluindo extração do ZIP e criação da estrutura."""
        output_dir = self.test_dir / "output"
        main(str(self.zip_path), str(output_dir))
        self.assertTrue((output_dir / "docusaurus/docs/Test Category/test_article.md").exists(), "O fluxo principal de migração falhou ao mover e converter o artigo.")

if __name__ == '__main__':
    unittest.main()
