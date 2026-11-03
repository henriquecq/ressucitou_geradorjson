import 'dart:io';
import '../lib/catalog_output.dart';

void main() {
  final temporary = Directory.systemTemp.createTempSync('ressuscitou-version-');
  try {
    final version = File('${temporary.path}/cantos_versao.txt');
    void expectVersion(String expected) {
      if (version.readAsStringSync().trim() != expected) {
        throw StateError('Expected revision $expected');
      }
    }

    writeCatalog(temporary.path, '{\n"edicao": 2026\n}');
    expectVersion('1');
    writeCatalog(temporary.path, '{\r\n"edicao": 2026\r\n}');
    expectVersion('1');
    writeCatalog(temporary.path, '{"edicao":2026,"cantos":[]}');
    expectVersion('2');
    writeCatalog(temporary.path, '{"edicao":2026,"cantos":[]}');
    expectVersion('2');
    version.writeAsStringSync('invalid');
    try {
      writeCatalog(temporary.path, 'must not be written');
      throw StateError('Invalid revision was accepted');
    } on FormatException {
      if (File('${temporary.path}/cantos.json').readAsStringSync() !=
          '{"edicao":2026,"cantos":[]}') {
        throw StateError('Catalog changed despite invalid revision');
      }
    }
    print('Catalog revision: initialization, changes, stable regeneration and invalid input passed.');
  } finally {
    temporary.deleteSync(recursive: true);
  }
}
