using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace C_Sharp
{
    static class ArrayFunc
    {
        static void ArrBasic()
        {
            // Single Dimentional Array
            int[] ar = new int[4];
            ar = new int[] { 1, 2, 3, 4 };
            Console.Write("1D Array: ");
            foreach (int i in ar) { Console.Write($"{i},"); }


            // Two Diamentional Array
            int[,] ar2D = new int[2, 2];
            ar2D = new int[,] { { 1, 2 }, { 3, 4 } };
            Console.Write("\n2D Array: ");
            foreach (int i in ar2D) { Console.Write($"{i},"); }

            // Three Diamentional Array
            int[,,] ar3D = new int[3, 2, 1] // Let ar3D = new int[X, Y, Z]
            {
                // Since X = 3, ar3D = int[3, X = int[2], Z = int[1]]
                {
                    // Since Y = 2, ar3D[0] = int [2, Z = int[1]]
                    {1}, {2}
                },
                {
                    {3}, {4}
                },
                {
                    {5}, {6}
                }
            };
            Console.Write("\n3D Array: ");
            foreach (int i in ar3D) { Console.Write($"{i},"); }

            // Jagged Array
            int[][] arJag = new int[3][];
            arJag[0] = new int[] { 1 };
            arJag[1] = new int[] { 2, 2 };
            arJag[2] = new int[] { 3, 3, 3 };
            Console.Write("\nJagged Array: ");
            for (int i = 0; i < arJag.Length; i++)
            {
                for (int j = 0; j < arJag[i].Length; j++)
                {
                    Console.Write($"{arJag[i][j]},");
                }
            }
        }
    }
}
