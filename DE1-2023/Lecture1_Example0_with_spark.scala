val lines = sc.textFile("/home/ubuntu/i_have_a_dream.txt")
printf("First line:%s",lines.first())

val words = lines.map(line => line.split(' '))

val word_counts = words.map(w => w.length)

val total_words = word_counts.reduce(_+_)

printf("total words=%d",total_words)  

val lines_splitted = lines.map(line => line.split(' '))

print(lines_splitted.first())

val all_words = lines.flatMap(line => line.split(' '))

all_words.take(10)

all_words.filter(word => word.startsWith("d")).take(10)