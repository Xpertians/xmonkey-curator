 ---
  🚨 DEPRECATION NOTICE: xmonkey-curator

  Project Status: ARCHIVED

  Effective Date: August 2025
  
  Reason: Superseded by Semantic Copycat BinarySniffer

  Migration Path

  xmonkey-curator functionality has been fully integrated and significantly enhanced in https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer.

  Feature Migration Mapping

  | xmonkey-curator Feature            | BinarySniffer Equivalent                 |
  |------------------------------------|------------------------------------------|
  | xmonkey-curator scan PATH          | binarysniffer analyze PATH               |
  | --unpack archive extraction        | ✅ Built-in (APK/IPA/JAR/ZIP/TAR)         |
  | --match-symbols signature matching | ✅ Core feature (90+ components)          |
  | --licenses license detection       | ✅ Built-in with comprehensive database   |
  | --output JSON export               | ✅ --format json --output file.json       |
  | --export-symbols symbol extraction | ✅ Enhanced symbol and pattern extraction |

  Why Migrate?

  🚀 Superior Performance

  - Multi-tier matching: Bloom filters → MinHash LSH → Database
  - Memory efficient: <100MB usage vs curator's higher overhead
  - Faster analysis: ~10-50ms per file after index loading

  🎯 Enhanced Detection

  - 42x improvement in component detection
  - Enhanced mode: --enhanced flag for comprehensive analysis
  - Confidence scoring: Detailed confidence percentages for matches

  📱 Mobile Specialization

  - APK analysis: AndroidManifest.xml, DEX files, native libraries
  - IPA analysis: Info.plist, frameworks, executables
  - Archive support: Nested archives, metadata extraction

  🗄️ Production Database

  - 90+ OSS components (vs curator's alpha signatures)
  - Real-world signatures: Facebook SDK, Jackson, FFmpeg, etc.
  - Automatic updates: Package-distributed signatures

  🛠️ Developer Experience

  - Stable API: Production-ready v1.3.0
  - Multiple outputs: Table, JSON, CSV formats
  - Python library: Programmatic usage support
  - Comprehensive docs: User guide, API reference

  Quick Migration Examples

  # xmonkey-curator (deprecated)
  xmonkey-curator scan app.apk --unpack --match-symbols --licenses --output results.json

  # BinarySniffer (recommended)
  binarysniffer analyze app.apk --enhanced --format json --output results.json

  Support Timeline

  - Immediate: xmonkey-curator archived, no new features
  - 30 days: Migration support and documentation
  - 90 days: Repository marked read-only

  Get Started

  # Install BinarySniffer
  pip install semantic-copycat-binarysniffer

  # Verify installation
  binarysniffer --version

  # Analyze your first file
  binarysniffer analyze /path/to/binary --enhanced

  Resources

  - 📖 Documentation: https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer/blob/main/docs/USER_GUIDE.md
  - 🐛 Issues: https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer/issues
  - 💬 Migration Help: Open an issue with migration label

  ---
  Thank you for using xmonkey-curator. We're excited to provide you with a more powerful and efficient solution in BinarySniffer! 🎉

