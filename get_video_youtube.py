from pytube import YouTube, Playlist
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, filedialog
import os
from moviepy.editor import *
from time import *
from random import randrange


window = tk.Tk()
window.iconbitmap("icon.ico")
window.title("Get Videos YouTube")
window.geometry("490x560")
window.resizable(True, True)
window.configure(bg="#121212")

link_var = tk.StringVar()
playlist_var = tk.StringVar()
download_path = tk.StringVar()
save_in = tk.StringVar()
statuss = tk.StringVar()
statuss2 = tk.StringVar()

global varBarra
varBarra = tk.DoubleVar()
varBarra.set(0)
varBarra2 = tk.DoubleVar()
varBarra2.set(0)
global pb
global pb2
global is_playlist
is_playlist = 0


def salvar_em(*args):
    statuss.set("Status")
    lbl_status["fg"] = "#313131"
    varBarra.set(0)
    statuss2.set("Status")
    lbl_status2["fg"] = "#313131"
    varBarra2.set(0)
    window.update()
    global download_Directory
    download_Directory = filedialog.askdirectory(initialdir='::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',
                                                 title="Selecione a pasta para salvar o vídeo ou audio")
    download_path.set(download_Directory)
    browse.delete(0, 'end')
    browse.insert(0, download_Directory)
    if download_Directory == "" or download_Directory is None:
        browse.delete(0, 'end')
        browse.insert(0, "Salvar em...")


def click_link(*args):
    statuss.set("Status")
    lbl_status["fg"] = "#313131"
    varBarra.set(0)
    statuss2.set("Status")
    lbl_status2["fg"] = "#313131"
    varBarra2.set(0)
    window.update()
    if link.get() == "" or link.get() == "Link":
        link.delete(0, 'end')


def leave_link(*args):
    if link.get() == "" or link.get() == "Link":
        link.delete(0, 'end')
        link.insert(0, 'Link')
        window.focus()


def click_playlist(*args):
    if playlist.get() == "" or playlist.get() == "Playlist":
        playlist.delete(0, 'end')


def leave_playlist(*args):
    if playlist.get() == "" or playlist.get() == "Playlist":
        playlist.delete(0, 'end')
        playlist.insert(0, 'Playlist')
        window.focus()


def progress(chunk, file_handle, bytes_remaining):
    remaining = (bytes_remaining * 100) / filesize
    step = 100 - int(remaining)
    varBarra.set(step)
    pb = ttk.Progressbar(window, variable=varBarra, maximum=100, length=450)
    pb.grid(row=6, column=0)
    print(f"Completed: {step}%")
    if is_playlist == 1:
        statuss.set(f"Baixando:\n{stream.title}\n{step}%")
    else:
        statuss.set(f"Baixando ({step}%):\n{youtube.title}")
    window.update()


def complete(chunk, path):
    print("Download concluído!")
    varBarra.set(100)
    pb = ttk.Progressbar(window, variable=varBarra, maximum=100, length=450)
    pb.grid(row=6, column=0)
    lbl_status["fg"] = "#00cc0e"
    statuss.set("Download concluído!")
    window.update()


# Funções para baixar
def baixar_video(*args):
    is_playlist = 0
    if browse.get() != "" and browse.get() != "Salvar em...":
        print(f"Diretório: {browse.get()}")
        if download_Directory is not None or download_Directory != "" or download_Directory != "Link":
            global youtube
            statuss.set(f"Conectando...")
            lbl_status["fg"] = "#cca300"
            youtube = YouTube(str(link.get()), on_progress_callback=progress, on_complete_callback=complete)
            my_video = youtube.streams.filter(progressive=True, file_extension='mp4').first()
            global filesize
            filesize = my_video.filesize
            statuss.set("Baixando...")
            lbl_status["fg"] = "#005ccc"
            print("Baixando...")
            my_video.download(f"{browse.get()}")
            window.update()


def baixar_audio(*args):
    is_playlist = 0
    if browse.get() != "" and browse.get() != "Salvar em...":
        print(f"Diretório: {browse.get()}")

        if download_Directory != None or download_Directory != "" or download_Directory != "Link":
            global youtube
            statuss.set(f"Conectando...")
            lbl_status["fg"] = "#cca300"
            youtube = YouTube(str(link.get()), on_progress_callback=progress, on_complete_callback=complete)
            # print(f"{youtube.streams.all()}")
            my_audio = youtube.streams.filter(only_audio=True).all()
            global filesize
            filesize = my_audio[0].filesize
            statuss.set(f"Baixando:\n{youtube.title}")
            lbl_status["fg"] = "#005ccc"
            print(f"Baixando:\n{youtube.title}")
            out_file = my_audio[0].download(output_path=f"{browse.get()}", filename_prefix=str(randrange(9999)))
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            # Verificar se existe um .mp3 na pasta com o mesmo nome, se sim, salva com outro nome
            if os.path.isfile(new_file):
                base, ext = os.path.splitext(out_file)
                new_file = f"{base}[{str(randrange(9999))}].mp3"
                os.rename(out_file, new_file)
            else:
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)

            statuss.set("Download concluído!")
            lbl_status["fg"] = "#00cc0e"
            print("Download concluído!")
            window.update()


def baixar_videos(*args):
    is_playlist = 1
    if browse.get() != "" and browse.get() != "Salvar em...":
        print(f"Diretório: {browse.get()}")
        if download_Directory is not None or download_Directory != "":
            PLAYLIST_URL = str(playlist.get())
            p = Playlist(PLAYLIST_URL)
            print(f'Downloading: {p.title}')
            print("Baixando...")
            cont = 0
            for url in p:
                remaining = (cont * 100) / len(p)
                # step = 100 - int(remaining)
                varBarra2.set(remaining)
                pb2 = ttk.Progressbar(window, variable=varBarra2, maximum=100, length=450)
                pb2.grid(row=13, column=0)
                print(f"Completed: {int(remaining)}%")  # show the percentage of completed download
                statuss2.set(f"Conectando...")
                lbl_status2["fg"] = "#cca300"
                video = YouTube(url)
                global stream
                stream = video.streams.get_highest_resolution()
                global filesize
                filesize = stream.filesize
                statuss2.set(f"Baixando({int(remaining)}%):\n{stream.title}")
                lbl_status2["fg"] = "#005ccc"
                stream.download(output_path=f"{browse.get()}/{p.title}")
                cont = cont + 1
                window.update()

            print('Downloading: 100%')
            varBarra2.set(100)
            statuss2.set("Download concluído!")
            lbl_status2["fg"] = "#00cc0e"
            window.update()


def baixar_audios(*args):
    is_playlist = 1
    if browse.get() != "" and browse.get() != "Salvar em...":
        print(f"Diretório: {browse.get()}")
        if download_Directory is not None or download_Directory != "":
            PLAYLIST_URL = str(playlist.get())
            p = Playlist(PLAYLIST_URL)
            print(f'Downloading: {p.title}')
            print("Baixando...")
            cont = 0
            for url in p:
                print(cont)
                remaining = (cont * 100) / len(p)
                # step = 100 - int(remaining)
                varBarra2.set(remaining)
                pb2 = ttk.Progressbar(window, variable=varBarra2, maximum=100, length=450)
                pb2.grid(row=13, column=0)
                # pb2.place(x=30, y=440, width=430, height=10)
                print(f"Completed: {int(remaining)}%")  # show the percentage of completed download
                statuss2.set(f"Conectando...")
                lbl_status2["fg"] = "#cca300"
                video = YouTube(url)
                global stream
                stream = video.streams.filter(only_audio=True).first()
                global filesize
                filesize = stream.filesize
                statuss2.set(f"Baixando({int(remaining)}%):\n{stream.title}")
                lbl_status2["fg"] = "#005ccc"
                out_file = stream.download(output_path=f"{browse.get()}/{p.title}",
                                           filename_prefix=str(randrange(9999)))
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                cont = cont + 1
                window.update()

            print('Downloading: 100%')
            varBarra2.set(100)
            statuss2.set("Download concluído!")
            lbl_status2["fg"] = "#00cc0e"
            window.update()


imagem1px = tk.PhotoImage(width=1, height=1)
fontbutton = tkFont.Font(family="Montserrat", size=9)
fontentry = tkFont.Font(family="Montserrat", size=11)

# espaço horizontal
fspaceL = tk.Frame(bg="#121212", width=490, height=22)
fspaceL.grid(row=0, column=0, columnspan=3)

frame_browse = tk.Frame(window, bg="#303030")
browse = tk.Entry(frame_browse, text='Link', bg="#121212", fg="#313131", font=fontentry, borderwidth=12, relief=tk.FLAT,
                  width=40, textvariable=save_in)
# Adicionando placeholder
browse.insert(0, 'Salvar em...')
browse.grid(row=1, column=0, columnspan=3, padx=1, pady=1)
frame_browse.grid(row=1, column=0, columnspan=3, padx=10, pady=0)

# Bind para simular placeholder
browse.bind("<Button-1>", salvar_em)

frame_link = tk.Frame(window, bg="#303030")
link = tk.Entry(frame_link, text='Link', bg="#121212", fg="#313131", font=fontentry, borderwidth=12, relief=tk.FLAT,
                width=40, textvariable=link_var)
# Adicionando placeholder
link.insert(0, 'Link')
link.grid(row=2, column=0, columnspan=3, padx=1, pady=1)
frame_link.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Bind para simular placeholder
link.bind("<Button-1>", click_link)
link.bind("<Leave>", leave_link)

# espaço horizontal
fspaceL2 = tk.Frame(bg="#121212", width=490, height=15)
fspaceL2.grid(row=3, column=0, columnspan=3)

# espaço vertical inicio botao video
fspaceinicio_video = tk.Frame(bg="#121212", width=490, height=15)
fspaceinicio_video.grid(row=4, column=0)

frame_botoes = tk.Frame(window, bg="#121212")
btn_video = tk.Button(frame_botoes, text="DOWNLOAD \nVIDEO", font=fontbutton, image=imagem1px, compound="c",
                      bg="#cc0000", fg="#FFF", width=133, height=37, highlightbackground="#35F2DF",
                      highlightcolor="#35F2DF", command=baixar_video)

frame_botoes.grid(row=4, column=0)
btn_video.grid(row=4, column=0)

frame_espaco_entre_botoes = tk.Frame(frame_botoes, bg="#121212", width=25, height=22)
frame_espaco_entre_botoes.grid(row=4, column=1)

btn_audio = tk.Button(frame_botoes, text="DOWNLOAD \nAUDIO", font=fontbutton, image=imagem1px, compound="c",
                      bg="#005ccc", fg="#FFF", width=133, height=37, highlightbackground="#35F2DF",
                      highlightcolor="#35F2DF", command=baixar_audio)

btn_audio.grid(row=4, column=2)

# espaço horizontal
fspace_antes_status = tk.Frame(bg="#121212", width=490, height=10)
fspace_antes_status.grid(row=5, column=0, columnspan=3)

statuss.set("Status")
lbl_status = tk.Label(window, textvariable=statuss, bg="#121212", fg="#313131", font="Montserrat 9", width="60", bd=1,
                      padx=0, pady=0)


lbl_status.grid(row=7, column=0)

# espaço horizontal
fspaceL2 = tk.Frame(bg="#121212", width=490, height=40)
fspaceL2.grid(row=8, column=0, columnspan=3)

# Frame Playlist ###
frame_playlist = tk.Frame(window, bg="#303030")
playlist = tk.Entry(frame_playlist, text='Link', bg="#121212", fg="#313131", font=fontentry, borderwidth=12,
                    relief=tk.FLAT, width=40, textvariable=playlist_var)
playlist.insert(0, 'Playlist')
playlist.grid(row=9, column=0, columnspan=3, padx=1, pady=1)
frame_playlist.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Bind para simular placeholder
playlist.bind("<Button-1>", click_playlist)
playlist.bind("<Leave>", leave_playlist)

# espaço horizontal
fspaceL2 = tk.Frame(bg="#121212", width=490, height=15)
fspaceL2.grid(row=10, column=0, columnspan=3)

frame_botoes2 = tk.Frame(window, bg="#121212")
btn_videos = tk.Button(frame_botoes2, text="DOWNLOAD \nVIDEOS", font=fontbutton, image=imagem1px, compound="c",
                       bg="#cc0000", fg="#FFF", width=133, height=37, highlightbackground="#35F2DF",
                       highlightcolor="#35F2DF", command=baixar_videos)

frame_botoes2.grid(row=11, column=0)
btn_videos.grid(row=11, column=0)

frame_espaco_entre_botoes2 = tk.Frame(frame_botoes2, bg="#121212", width=25, height=22)
frame_espaco_entre_botoes2.grid(row=9, column=1)

btn_audios = tk.Button(frame_botoes2, text="DOWNLOAD \nAUDIOS", font=fontbutton, image=imagem1px, compound="c",
                       bg="#005ccc", fg="#FFF", width=133, height=37, highlightbackground="#35F2DF",
                       highlightcolor="#35F2DF", command=baixar_audios)

btn_audios.grid(row=11, column=2)

# espaço horizontal
fspace_antes_status2 = tk.Frame(bg="#121212", width=490, height=10)
fspace_antes_status2.grid(row=12, column=0, columnspan=3)

statuss2.set("Status")
lbl_status2 = tk.Label(window, textvariable=statuss2, bg="#121212", fg="#313131", font="Montserrat 9", width="60", bd=1,
                       padx=0, pady=0)

lbl_status2.grid(row=14, column=0)

window.mainloop()
