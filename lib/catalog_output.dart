import 'dart:io';

// The revision is a decimal integer, independent of the book edition.
void writeCatalog(String directory, String content) {
  final catalog = File('$directory/cantos.json');
  final version = File('$directory/cantos_versao.txt');
  final previousVersion = version.existsSync()
      ? int.tryParse(version.readAsStringSync().trim())
      : 0;
  if (previousVersion == null || previousVersion < 0) {
    throw FormatException('cantos_versao.txt must contain a non-negative integer');
  }
  final normalized = content.replaceAll('\r\n', '\n');
  final changed = !catalog.existsSync() ||
      catalog.readAsStringSync().replaceAll('\r\n', '\n') != normalized;
  final revision = previousVersion == 0 ? 1 : previousVersion + (changed ? 1 : 0);
  catalog.writeAsStringSync(normalized.replaceAll('\n', '\r\n'));
  version.writeAsStringSync('$revision\n');
}
