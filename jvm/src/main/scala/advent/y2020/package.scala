package advent

import advent.shared.InputTransformer

package object y2020 {
  implicit val inputTransformerForId: InputTransformer[String] =
    InputTransformer.id()
}
