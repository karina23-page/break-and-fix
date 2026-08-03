resource "aws_key_pair" "movies" {
  key_name   = "movies"
  public_key = file("${path.root}/movies.pub")
}

module "movie" {
  source = "./modules/app"

  key_name = aws_key_pair.movies.key_name

}

module "jenkins" {
  source = "./modules/jenkins"

  key_name = aws_key_pair.movies.key_name

}