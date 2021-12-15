// Scala program to multiply two matrices

object Sample {
  def main(args: Array[String]) {
    var Matrix1 = Array.ofDim[Int](2, 2)
    var Matrix2 = Array.ofDim[Int](2, 2)
    var Matrix3 = Array.ofDim[Int](2, 2)

    var i: Int = 0
    var j: Int = 0
    var k: Int = 0

    var sum: Int = 0

    printf("Enter elements of MATRIX1:\n")
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        printf("ELEMENT(%d)(%d): ", i, j);
        Matrix1(i)(j) = scala.io.StdIn.readInt();
        j = j + 1;
      }
      i = i + 1;
    }

    printf("Enter elements of MATRIX2:\n")
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        printf("ELEMENT(%d)(%d): ", i, j);
        Matrix2(i)(j) = scala.io.StdIn.readInt();
        j = j + 1;
      }
      i = i + 1;
    }

    //Multiply Matrix1 and Matrix2
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        sum = 0;
        k = 0;
        while (k < 2) {
          sum = sum + (Matrix1(i)(k) * Matrix2(k)(j));
          k = k + 1;
        }
        Matrix3(i)(j) = sum;
        j = j + 1;
      }
      i = i + 1;
    }

    printf("MATRIX1:\n")
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        printf("%d ", Matrix1(i)(j));
        j = j + 1;
      }
      i = i + 1;
      println();
    }

    printf("MATRIX2:\n")
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        printf("%d ", Matrix2(i)(j));
        j = j + 1;
      }
      i = i + 1;
      println();
    }

    printf("Multiplication of Matrix1 and Matrix2:\n")
    i = 0;
    while (i < 2) {
      j = 0;
      while (j < 2) {
        printf("%d ", Matrix3(i)(j));
        j = j + 1;
      }
      i = i + 1;
      println();
    }
  }
}