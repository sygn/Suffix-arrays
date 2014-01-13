using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Diagnostics;

namespace Manber_Myers_SA
{
    class Program
    {
        static void Main(string[] args)
        {
           
            string text = "";
            bool success = false;
            try
            {
                text = ReadText(args[0]);
                success = true;
            }
            catch
            {
                Console.WriteLine("Error during file reading! Please check your input file!");
                success = false;
            }

            if (success)
            {
                try
                {
                    DoIt(text);
                }
                catch
                {
                    Console.WriteLine("Something has gone wrong! Please check your input txt file!");
                }
            }
        }

        static void DoIt(string text)
        {

            /* Arrays that will be used by algorithm */
            #region Variables

            int[] POS = new int[text.Length];       //Suffix Array (Output)
            int[] PRM = new int[text.Length];       //Inverse Suffix Array (PRM[POS[i]] = i)
            bool[] BH = new bool[text.Length];      //Points to the leftmost suffix of a H-bucket
            bool[] B2H = new bool[text.Length];     //Marks moved suffixes; After checking, points to the leftmost suffix in 2H-bucket
            int[] Count = new int[text.Length];     //Internal array
            int[] next = new int[text.Length];      //Internal array
            Stopwatch stopWatch = new Stopwatch();  //Stopwatch for measuring algorithm's time
             Process currentProc = Process.GetCurrentProcess(); //Memory monitor
            #endregion

            stopWatch.Start();

            /*
             * This section sets all arrays according to the first stage
             * Sets all the suffixes according to their first letter (Sets POS, PRM and BH arrays)
             * */
            #region First Phase Bucket Sort

            Dictionary<char, int> Alphabet = new Dictionary<char, int>();
            int t = 0;
            foreach (char x in text)
            {
                if (Alphabet.Keys.Contains(x))
                    Alphabet[x]++;
                else
                    Alphabet.Add(x, 1);
                POS[t] = -1;
                BH[t] = false;
                B2H[t] = false;
                Count[t] = 0;
                t++;
            }
            var Letters = Alphabet.Keys.ToList();
            Letters.Sort();

            int letterFirstposition;
            int letterOffset;
            int letterposition = 0;
            BH[0] = true;
            foreach (char x in text)
            {
                letterFirstposition = 0;
                foreach (char y in Letters)
                {
                    if (x != y)
                    {
                        letterFirstposition += Alphabet[y];
                    }
                    else
                        break;
                }

                letterOffset = letterFirstposition;
                BH[letterFirstposition] = true;
                while (POS[letterOffset] != -1)
                {
                    letterOffset++;
                }
                POS[letterOffset] = letterposition;
                PRM[letterposition] = letterOffset;
                letterOffset = 0;
                letterposition++;
            }
            #endregion


            /*
             * Algorithm by H=1,2,4,8,16...H<N
             * POS array and time elapsed are written in console after the sort is done
             * */
            #region Algorithm

            for (int h=1; h<text.Length; h=h*2)
            {
                int buckets = 0;
                for (int i=0, j; i<text.Length; i=j)
                {
                    j = i + 1;
                    while (j < text.Length && !BH[j])
                        j++;
                    next[i] = j;
                    buckets++;
                }

                if (buckets == text.Length)     //Algorithm is done after every suffix is in its own bucket
                    break;

                for (int i = 0; i<text.Length; i=next[i])       //Sets PRM array
                {
                    Count[i] = 0;
                    for (int j = i; j < next[i]; j++)
                        PRM[POS[j]] = i;
                }

                Count[PRM[text.Length - h]]++;
                B2H[PRM[text.Length - h]] = true;

                    for (int i = 0; i < text.Length; i = next[i])       //Scan all buckets and update PRM, Count and B2H arrays
                    {
                        for(int j=i; j<next[i]; j++)                    //Update arrays
                        {
                            int s = POS[j] - h;
                            if (s>=0)
                            {
                                int head = PRM[s];
                                PRM[s] = head + Count[head]++;
                                B2H[PRM[s]] = true;
                        }
                    }


                    for(int j=i; j<next[i]; j++)                //Reset B2H array such that only the leftmost of them in each
                    {                                           //2H-bucket is set to 1, and rest are reset to 0
                        int s = POS[j] - h;
                        if (s>=0 && B2H[PRM[s]])
                        {
                            for (int k = (PRM[s] + 1); k<findnextbh(k, BH, text.Length); k++)
                                B2H[k] = false;
                        }
                    }
                }

                for (int i=0; i<text.Length; i++)           //Updating POS and BH arrays
                {
                    POS[PRM[i]] = i;
                    BH[i] |= B2H[i];
                }

            }

            for (int i=0; i<text.Length; i++)           //Updating PRM array
            {
                PRM[POS[i]] = i;
            }

            stopWatch.Stop();

            try
            {
                SaveSAToFile(POS, PRM);
            }
            catch
            {
                Console.WriteLine("Something went wrong during saving SA to file. Check if you are Administrator user on this PC maybe.");
            }

            Console.WriteLine("\nSA created in " + stopWatch.Elapsed.TotalSeconds+ " seconds\n and saved to SAOutput.txt file");
            Console.WriteLine("\n Total memory consumption in bytes: " + currentProc.PrivateMemorySize64);
            Console.WriteLine("\n!!!----------------NOTE----------------!!!");
            Console.WriteLine("If your input txt file has any other characters but letters, this SA is invalid and you should check your input file!");
            #endregion
        }

        /// <summary>
        /// Finding position of next true value in BH array starting from x
        /// </summary>
        /// <param name="x">Starting position</param>
        /// <param name="BH">BH array</param>
        /// <param name="end">Last position in BH array</param>
        /// <returns>Int position of next true value in BH array or latest possible index</returns>
        static int findnextbh(int x, bool[] BH, int end)
        {
            for (int i=x; i<end; i++)
            {
                if (BH[i] == true)
                    return i;
            }
            return end;
        }

        static string ReadText(string path)
        {
            string text = "";
            string[] lines = File.ReadAllLines(path);
            foreach (string line in lines)
                text = text + line;
            text.ToUpper();
            return text;
        }

        static void SaveSAToFile(int[] POS, int[]PRM)
        {
            using (StreamWriter w = File.AppendText("SAOutput.txt"))
            {
                w.WriteLine("   ");
                w.WriteLine("------------------------------------------------------------------------");
                w.WriteLine(DateTime.Now.ToString());
                w.WriteLine("SA");
                w.Write("[");
                foreach (int i in POS)
                    w.Write(i+", ");
                w.Write("]");
                w.WriteLine("\n");
                w.WriteLine("PRM (inverse SA)");
                w.Write("[");
                foreach (int i in PRM)
                    w.Write(i + ", ");
                w.Write("]");
            }
                
        }
    }
}
