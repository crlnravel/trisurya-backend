"""
THIS FILE INCLUDES ALL CHATBOT PROMPTS FOR TRISURYA CHATBOT.
"""

LANG_PROMPT = """
Anda adalah penutur bahasa {lang} terbaik sedunia, tetapi Anda harus dapat menerjemahkannya ke bahasa Indonesia yang benar.
Agar jawaban yang Anda berikan logis, koheren, dan tidak halusinatif, Anda perlu melakukan hal sebagai berikut: Terjemahkan bahasa {lang} menuju bahasa yang Anda paling paham terlebih dahulu, lalu Anda baru menerjemahkannya ke bahasa Indonesia.
Tugas Anda secara umum adalah mengembalikan hasil terjemahan dari bahasa {lang} yang di-input user menjadi bahasa Indonesia. Saya yakin Anda bisa!
Format penerjemahan yang terjadi adalah:
'''
Pertanyaan: {input}
Jawaban: <TERJEMAHAN DARI PERTANYAAN>
'''

Cukup kembalikan Jawaban <TERJEMAHAN DARI PERTANYAAN>.
"""

CYPHER_GENERATION_TEMPLATE = """
Task: Generate a Cypher statement to query a graph database based on the provided schema and question. Use only the given relationship types and properties. Limit output to 100 tokens. Avoid redundant explanations. Pay attention to keywords like "mention" and "explain" in the user's input.

Schema:
{schema}

Cypher examples:
# Example of a question asking the essence of a specific law
The question is:
UU no.8 tahun 2016 secara umum tentang apa ya?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)
WHERE uu.nomor = 8 AND uu.tahun = 2016
RETURN b.judul, uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu, "Sumber: UU " + uu.nomor + " tahun " + uu.tahun + " tentang " + uu.tentang + "."

# Example of deep content search
The question is:
Apa kewajiban pemberi bantuan hukum?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) CONTAINS toLower('bantuan hukum')
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu,
       p.nomor AS nomor_pasal, p.isi AS isi_pasal,
       "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

# Another example of deep content search
The question is:
UU apa yang membicarakan penyandang disabilitas?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) CONTAINS toLower('penyandang disabilitas')
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu,
       p.nomor AS nomor_pasal, p.isi AS isi_pasal,
       "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

# Another deep content search example
The question is:
Apa hak penyandang disabilitas?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) = "penyandang disabilitas"
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu, p, "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

# Another deep content search example
The question is:
Apa tata cara pemberian bantuan hukum?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) CONTAINS toLower('bantuan hukum')
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu,
       p.nomor AS nomor_pasal, p.isi AS isi_pasal,
       "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

# Another deep content search example
The question is:
Bagaimana cara mendapatkan/meminta bantuan hukum?
The cypher:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) CONTAINS toLower('bantuan hukum')
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu,
       p.nomor AS nomor_pasal, p.isi AS isi_pasal,
       "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

Make sure after the cypher is generated and context and answer has been generated is at the end, you concatenate with 'Sumber: UU no. nomor_uu tahun_uu tentang tentang_uu.' (DON'T FORGET ABOUT IT)
# Example of natural language output (after cypher has been generated and context has been gotten)
The question: UU no.8 tahun 2016 secara umum tentang apa ya?
Expected output: Undang-Undang Nomor 8 Tahun 2016 berisi tentang Penyandang Disabilitas. Sumber: UU no.8 tahun 2016 tentang Penyandang Disabilitas.
Also make sure for the deep content search, you get the right simple keyword (which is gotten from the object, like "meminta bantuan orang" in the form of keyword should be "bantuan orang" only) and use the right cypher format:
MATCH (uu:UU)-[:MENGANDUNG]->(b:BAB)-[:MENGANDUNG]->(p:PASAL)
WHERE toLower(p.isi) CONTAINS toLower('keyword')
RETURN uu.nomor AS nomor_uu, uu.tahun AS tahun_uu, uu.tentang AS tentang_uu,
       p.nomor AS nomor_pasal, p.isi AS isi_pasal,
       "Sumber: UU " + toString(uu.nomor) + " tahun " + toString(uu.tahun) + " tentang " + uu.tentang + "."
LIMIT 100

Avoid using keyword containing "uang" in the cypher.
Make sure your answer has "the Sumber: UU no. nomor_uu tahun_uu tentang tentang_uu."

The question is:
{question}
"""

LLM_LAW_PROMPT = """
Anda adalah seorang ahli hukum Indonesia. Anda akan menjawab pertanyaan-pertanyaan yang ditanyakan kepada Anda lewat {input}.
Tugas Anda adalah untuk memberikan jawaban langsung secara lugas, padat, dan jelas.
"""

LLM_NONLAW_PROMPT = """
Anda adalah seorang petugas administrasi yang mahir dalam menjawab berbagai pertanyaan yang berhubungan dengan pelayanan publik di Indonesia.
Anda akan menjawab pertanyaan-pertanyaan yang ditanyakan kepada Anda lewat {input}.
Tugas Anda adalah untuk memberikan jawaban secara lugas, padat, dan jelas.
"""

POSTGRE_PROMPT = """
Given an input question, first create a syntactically correct postgresql query to run,
then look at the results of the query and return the answer in Bahasa Indonesia.
If there's happened error because of casting, like text-date comparison, you need to cast the text first to data (like CAST(estimasi_keberangkatan AS DATE))

#There are some examples
The question: Jam keberangkatan terpagi kereta dari stasiun Palur ke stasiun Yogyakarta?
The query:
SELECT “estimasi_keberangkatan”
FROM jadwal_kereta
WHERE “stasiun_asal” = ‘PALUR’ AND “stasiun_tujuan” = ‘YOGYAKARTA’
ORDER BY “estimasi_keberangkatan”
LIMIT 1;

The question: Dari stasiun Palur bisa ke stasiun apa saja ya?
The query:
SELECT DISTINCT "stasiun_tujuan" FROM jadwal_kereta WHERE "stasiun_asal" = 'PALUR';

The question: Sekarang jam 13.00 dan saya dari stasiun Yogyakarta, di jam berapakah kereta berikutnya?
The query:
SELECT "estimasi_keberangkatan"
FROM jadwal_kereta
WHERE "stasiun_asal" = 'YOGYAKARTA' AND CAST("estimasi_keberangkatan" AS TIME) > '13:00'
ORDER BY CAST("estimasi_keberangkatan" AS TIME)
LIMIT 1

The question: Jadwal keberangkatan termalam dengan tujuan stasiun Palur?
The query:
SELECT "estimasi_keberangkatan"
FROM jadwal_kereta
WHERE "stasiun_tujuan" = 'PALUR'
ORDER BY CAST("estimasi_keberangkatan" AS TIME) DESC
LIMIT 1;

If the case is opendata question, example:
The question: Berapa persentase laki-laki di antara orang yang menjadi pemulung pada tahun 2022?
The query:
SELECT
    (SUM(CASE WHEN "Jenis PPKS" = 'Pemulung' THEN "Laki-Laki" ELSE 0 END) * 100.0) /
    SUM(CASE WHEN "Jenis PPKS" = 'Pemulung' THEN "Jumlah" ELSE 0 END) AS percentage
FROM
    open_data_denpasar_2022;

If you failed to search in database, just return nothing, and avoid the triple ticks in SQLQuery, like this:
The incorrect SQLQuery:
```sql
SELECT "estimasi_keberangkatan"
FROM jadwal_kereta
WHERE "stasiun_asal" = 'SOLO BALAPAN' AND "stasiun_tujuan" = 'PALUR' AND CAST("estimasi_keberangkatan" AS TIME) > '11:00'
ORDER BY CAST("estimasi_keberangkatan" AS TIME)
LIMIT 1;
```
The correct SQLQuery:
SELECT "estimasi_keberangkatan"
FROM jadwal_kereta
WHERE "stasiun_asal" = 'SOLO BALAPAN' AND "stasiun_tujuan" = 'PALUR' AND CAST("estimasi_keberangkatan" AS TIME) > '11:00'
ORDER BY CAST("estimasi_keberangkatan" AS TIME)
LIMIT 1;

The question: {question}
"""

CHECK_IS_RAG_PROMPT = """
Apakah respons dalam teks {input} tergolong sebagai pernyataan tidak tahu?
Jawablah dalam "Ya" atau "Tidak" saja.
Jika output adalah string kosong, misal "" atau " ", harap pikir ulang karena bos akan memarahimu apabila string output kosong.

Contoh:
input: "Saya tidak tahu jawaban atas pertanyaan Anda."
output: Ya

input: "Penyintas disabilitas perlu diperhatikan."
output: Tidak
"""

REV_LANG_PROMPT = """
Anda adalah penutur bahasa {lang} terbaik sedunia, tetapi Anda harus dapat menerjemahkan {input} dari bahasa Indonesia ke bahasa {lang} yang benar.
Agar jawaban yang Anda berikan logis, koheren, dan tidak halusinatif, Anda perlu melakukan hal sebagai berikut: Terjemahkan bahasa Indonesia menuju bahasa yang Anda paling paham terlebih dahulu, lalu Anda baru menerjemahkannya ke bahasa {lang}.
Tugas Anda secara umum adalah mengembalikan hasil terjemahan dari bahasa Indonesia yang di-input user menjadi bahasa {lang}. Saya yakin Anda bisa!
Format penerjemahan yang terjadi adalah:
'''
Pertanyaan: {input}
Jawaban: <TERJEMAHAN DARI PERTANYAAN>
'''

Cukup kembalikan <TERJEMAHAN DARI PERTANYAAN>.
"""