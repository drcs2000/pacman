import os

def rename_tile_to_board(folder_path):
    # Lista todos os arquivos na pasta
    files = os.listdir(folder_path)
    
    # Loop através dos arquivos e renomeia cada um
    for filename in files:
        # Verifica se "tile" está no nome do arquivo
        if "tile" in filename:
            # Substitui "tile" por "board"
            new_name = filename.replace("tile", "board")
            
            # Caminhos completos
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_name)
            
            # Renomeia o arquivo
            os.rename(old_file_path, new_file_path)
            print(f"{filename} renomeado para {new_name}")

# Exemplo de uso
folder_path = "Assets/BoardImages"
rename_tile_to_board(folder_path)
