from flask import Flask, request, render_template, send_file
from main import AsistenteOpenAi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    asistente = AsistenteOpenAi()  # Crear una nueva instancia de AsistenteOpenAi
    if 'myfile' not in request.files:
        return "No file part"

    file = request.files['myfile']

    if file.filename == '':
        return "No selected file"

    file.save('./audio/recibido/audio.mp3')  # Guardar el archivo en el sistema de archivos

    transcripcion = asistente.audio_to_text("./audio/recibido/audio.mp3")
    chat = asistente.generate_answer(transcripcion)
    asistente.generate_audio(chat, file_path="./audio/enviado/respuesta.mp3")

    return send_file('./audio/enviado/respuesta.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
