package advent.shared

trait InputTransformer[I] {
  def transformInput(line: String): I
}

object InputTransformer {
  def id(): InputTransformer[String] = new InputTransformer[String] {
    def transformInput(line: String): String = line
  }

  def apply[A](implicit instance: InputTransformer[A]): InputTransformer[A] =
    instance

  object implicits {
    implicit val inputTransformerForId: InputTransformer[String] =
      InputTransformer.id()
  }
}
