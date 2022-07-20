{
  __m512i r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, ra, rb, rc, rd, re, rf;
  __m512i t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, ta, tb, tc, td, te, tf;

  r0 = _mm512_loadu_si512(mat + 0*16);
  r1 = _mm512_loadu_si512(mat + 1*16);
  r2 = _mm512_loadu_si512(mat + 2*16);
  r3 = _mm512_loadu_si512(mat + 3*16);
  r4 = _mm512_loadu_si512(mat + 4*16);
  r5 = _mm512_loadu_si512(mat + 5*16);
  r6 = _mm512_loadu_si512(mat + 6*16);
  r7 = _mm512_loadu_si512(mat + 7*16);
  r8 = _mm512_loadu_si512(mat + 8*16);
  r9 = _mm512_loadu_si512(mat + 9*16);
  ra = _mm512_loadu_si512(mat + 10*16);
  rb = _mm512_loadu_si512(mat + 11*16);
  rc = _mm512_loadu_si512(mat + 12*16);
  rd = _mm512_loadu_si512(mat + 13*16);
  re = _mm512_loadu_si512(mat + 14*16);
  rf = _mm512_loadu_si512(mat + 15*16);

  t0 = _mm512_unpacklo_epi32(r0,r1); /*   0  16   1  17   4  20   5  21   8  24   9  25  12  28  13  29 */
  t1 = _mm512_unpackhi_epi32(r0,r1); /*   2  18   3  19   6  22   7  23  10  26  11  27  14  30  15  31 */
  t2 = _mm512_unpacklo_epi32(r2,r3); /*  32  48  33  49 ... */
  t3 = _mm512_unpackhi_epi32(r2,r3); /*  34  50  35  51 ... */
  t4 = _mm512_unpacklo_epi32(r4,r5); /*  64  80  65  81 ... */
  t5 = _mm512_unpackhi_epi32(r4,r5); /*  66  82  67  83 ... */
  t6 = _mm512_unpacklo_epi32(r6,r7); /*  96 112  97 113 ... */
  t7 = _mm512_unpackhi_epi32(r6,r7); /*  98 114  99 115 ... */
  t8 = _mm512_unpacklo_epi32(r8,r9); /* 128 ... */
  t9 = _mm512_unpackhi_epi32(r8,r9); /* 130 ... */
  ta = _mm512_unpacklo_epi32(ra,rb); /* 160 ... */
  tb = _mm512_unpackhi_epi32(ra,rb); /* 162 ... */
  tc = _mm512_unpacklo_epi32(rc,rd); /* 196 ... */
  td = _mm512_unpackhi_epi32(rc,rd); /* 198 ... */
  te = _mm512_unpacklo_epi32(re,rf); /* 228 ... */
  tf = _mm512_unpackhi_epi32(re,rf); /* 230 ... */

  r0 = _mm512_unpacklo_epi64(t0,t2); /*   0  16  32  48 ... */
  r1 = _mm512_unpackhi_epi64(t0,t2); /*   1  17  33  49 ... */
  r2 = _mm512_unpacklo_epi64(t1,t3); /*   2  18  34  49 ... */
  r3 = _mm512_unpackhi_epi64(t1,t3); /*   3  19  35  51 ... */
  r4 = _mm512_unpacklo_epi64(t4,t6); /*  64  80  96 112 ... */
  r5 = _mm512_unpackhi_epi64(t4,t6); /*  65  81  97 114 ... */
  r6 = _mm512_unpacklo_epi64(t5,t7); /*  66  82  98 113 ... */
  r7 = _mm512_unpackhi_epi64(t5,t7); /*  67  83  99 115 ... */
  r8 = _mm512_unpacklo_epi64(t8,ta); /* 128 144 160 176 ... */
  r9 = _mm512_unpackhi_epi64(t8,ta); /* 129 145 161 178 ... */
  ra = _mm512_unpacklo_epi64(t9,tb); /* 130 146 162 177 ... */
  rb = _mm512_unpackhi_epi64(t9,tb); /* 131 147 163 179 ... */
  rc = _mm512_unpacklo_epi64(tc,te); /* 192 208 228 240 ... */
  rd = _mm512_unpackhi_epi64(tc,te); /* 193 209 229 241 ... */
  re = _mm512_unpacklo_epi64(td,tf); /* 194 210 230 242 ... */
  rf = _mm512_unpackhi_epi64(td,tf); /* 195 211 231 243 ... */

  t0 = _mm512_shuffle_i32x4(r0, r4, 0x88); /*   0  16  32  48   8  24  40  56  64  80  96  112 ... */
  t1 = _mm512_shuffle_i32x4(r1, r5, 0x88); /*   1  17  33  49 ... */
  t2 = _mm512_shuffle_i32x4(r2, r6, 0x88); /*   2  18  34  50 ... */
  t3 = _mm512_shuffle_i32x4(r3, r7, 0x88); /*   3  19  35  51 ... */
  t4 = _mm512_shuffle_i32x4(r0, r4, 0xdd); /*   4  20  36  52 ... */
  t5 = _mm512_shuffle_i32x4(r1, r5, 0xdd); /*   5  21  37  53 ... */
  t6 = _mm512_shuffle_i32x4(r2, r6, 0xdd); /*   6  22  38  54 ... */
  t7 = _mm512_shuffle_i32x4(r3, r7, 0xdd); /*   7  23  39  55 ... */
  t8 = _mm512_shuffle_i32x4(r8, rc, 0x88); /* 128 144 160 176 ... */
  t9 = _mm512_shuffle_i32x4(r9, rd, 0x88); /* 129 145 161 177 ... */
  ta = _mm512_shuffle_i32x4(ra, re, 0x88); /* 130 146 162 178 ... */
  tb = _mm512_shuffle_i32x4(rb, rf, 0x88); /* 131 147 163 179 ... */
  tc = _mm512_shuffle_i32x4(r8, rc, 0xdd); /* 132 148 164 180 ... */
  td = _mm512_shuffle_i32x4(r9, rd, 0xdd); /* 133 149 165 181 ... */
  te = _mm512_shuffle_i32x4(ra, re, 0xdd); /* 134 150 166 182 ... */
  tf = _mm512_shuffle_i32x4(rb, rf, 0xdd); /* 135 151 167 183 ... */

  r0 = _mm512_shuffle_i32x4(t0, t8, 0x88); /*   0  16  32  48  64  80  96 112 ... 240 */
  r1 = _mm512_shuffle_i32x4(t1, t9, 0x88); /*   1  17  33  49  66  81  97 113 ... 241 */
  r2 = _mm512_shuffle_i32x4(t2, ta, 0x88); /*   2  18  34  50  67  82  98 114 ... 242 */
  r3 = _mm512_shuffle_i32x4(t3, tb, 0x88); /*   3  19  35  51  68  83  99 115 ... 243 */
  r4 = _mm512_shuffle_i32x4(t4, tc, 0x88); /*   4 ... */
  r5 = _mm512_shuffle_i32x4(t5, td, 0x88); /*   5 ... */
  r6 = _mm512_shuffle_i32x4(t6, te, 0x88); /*   6 ... */
  r7 = _mm512_shuffle_i32x4(t7, tf, 0x88); /*   7 ... */
  r8 = _mm512_shuffle_i32x4(t0, t8, 0xdd); /*   8 ... */
  r9 = _mm512_shuffle_i32x4(t1, t9, 0xdd); /*   9 ... */
  ra = _mm512_shuffle_i32x4(t2, ta, 0xdd); /*  10 ... */
  rb = _mm512_shuffle_i32x4(t3, tb, 0xdd); /*  11 ... */
  rc = _mm512_shuffle_i32x4(t4, tc, 0xdd); /*  12 ... */
  rd = _mm512_shuffle_i32x4(t5, td, 0xdd); /*  13 ... */
  re = _mm512_shuffle_i32x4(t6, te, 0xdd); /*  14 ... */
  rf = _mm512_shuffle_i32x4(t7, tf, 0xdd); /*  15  31  47  63  79  96 111 127 ... 255 */

  _mm512_storeu_si512(matT + 0*16, r0);
  _mm512_storeu_si512(matT + 1*16, r1);
  _mm512_storeu_si512(matT + 2*16, r2);
  _mm512_storeu_si512(matT + 3*16, r3);
  _mm512_storeu_si512(matT + 4*16, r4);
  _mm512_storeu_si512(matT + 5*16, r5);
  _mm512_storeu_si512(matT + 6*16, r6);
  _mm512_storeu_si512(matT + 7*16, r7);
  _mm512_storeu_si512(matT + 8*16, r8);
  _mm512_storeu_si512(matT + 9*16, r9);
  _mm512_storeu_si512(matT + 10*16, ra);
  _mm512_storeu_si512(matT + 11*16, rb);
  _mm512_storeu_si512(matT + 12*16, rc);
  _mm512_storeu_si512(matT + 13*16, rd);
  _mm512_storeu_si512(matT + 14*16, re);
  _mm512_storeu_si512(matT + 15*16, rf);
}
