class Canto {
  int id;
  int categoria;
  List<String> categorias = [];
  String numero = '';
  late String htmlBase64;
  late String extBase64;
  String titulo;
  String html;
  String url;

  Canto(this.id, this.titulo, this.html, this.url, this.categoria);

  Canto.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        titulo = json['titulo'],
        html = json['html'],
        url = json['url'],
        categoria = json['categoria'],
        numero = json['numero'],
        categorias = List<String>.from(json['categorias']),
        htmlBase64 = json['html_base64'],
        extBase64 = json['ext_base64'];

  Map<String, dynamic> toJson() => {
    'id': id,
    'titulo': titulo,
    'html': html,
    'url': url,
    'categoria': categoria,
    'numero': numero,
    'categorias': categorias,
    'html_base64': htmlBase64,
    'ext_base64': extBase64,
  };
}
