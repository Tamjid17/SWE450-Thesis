for i in {1..100}; do
  uname=$(tr -dc 'a-z0-9' </dev/urandom | head -c $((5 + RANDOM % 10)))
  domain=$(shuf -n1 <<< "gmail.com yahoo.com protonmail.com outlook.com test.me mail.net")
  echo "email=${uname}@${domain}"
done
for i in {1..100}; do
  ip="$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256))"
  echo "ip=${ip}"
done
for i in {1..50}; do
  echo "card=$(openssl rand -hex 8)"
done
for i in {1..50}; do
  echo "cookie=$(openssl rand -hex 16)"
done

