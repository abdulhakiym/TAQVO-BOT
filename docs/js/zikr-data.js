/* TAQVO PRO MAX — zikrlar bazasi: 14 ta tonggi va 14 ta kechki zikr.
   Har bir zikr: arabcha (ar), o'qilishi (tr), o'zbekcha ma'nosi (uz), fazilati (fazl), manba (src), soni (n).
   Qur'on oyat va suralarining arabcha matni hamda tarjimasi (q) alquran.cloud API'dan olinadi, o'zgartirilmaydi.
   MUHIM: o'qilishi, ma'no va hadis raqamlari xotiradan yozilgan. Nashrdan oldin ishonchli manba
   (Hisnul Muslim, sunnah.com) va ustoz bilan tekshiring. Xato topsangiz, shu faylda to'g'rilang. */
(() => {
  const KURSI = { id: 'kursi', t: 'Oyatul Kursi', q: '2:255', n: 1,
    fazl: 'Qur’ondagi eng ulug‘ oyat. Uyquga yotganda o‘qigan kishiga Alloh tomonidan doimiy himoyachi bo‘lishi va shayton yaqinlasha olmasligi haqida hadis kelgan.',
    src: 'Qur’on 2:255; Buxoriy 2311' };
  const FAZL3 = 'Kim kechqurun va ertalab uch martadan o‘qisa, bu unga har narsadan kifoya qiladi.';
  const IKHLOS = { id: 'ikhlos', t: 'Ixlos surasi', q: 's112', n: 3, fazl: FAZL3, src: 'Qur’on 112; Abu Dovud 5082, Termiziy 3575',
    tr: 'Qul huvallohu ahad. Allohus-somad. Lam yalid va lam yuulad. Va lam yakun lahuu kufuvan ahad.' };
  const FALAQ = { id: 'falaq', t: 'Falaq surasi', q: 's113', n: 3, fazl: FAZL3, src: 'Qur’on 113; Abu Dovud 5082, Termiziy 3575',
    tr: 'Qul a’uuzu birobbil-falaq. Min sharri maa xolaq. Va min sharri g‘oosiqin izaa vaqab. Va min sharrin-naffaasaati fil-‘uqad. Va min sharri haasidin izaa hasad.' };
  const NOS = { id: 'nos', t: 'Nos surasi', q: 's114', n: 3, fazl: FAZL3, src: 'Qur’on 114; Abu Dovud 5082, Termiziy 3575',
    tr: 'Qul a’uuzu birobbin-naas. Malikin-naas. Ilaahin-naas. Min sharril-vasvaasil-xonnaas. Allaziy yuvasvisu fii suduurin-naas. Minal-jinnati van-naas.' };

  const SAYYID = { id: 'sayyid', t: 'Sayyidul istig‘for', n: 1,
    ar: 'اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ',
    tr: 'Allohumma anta Robbiy, laa ilaaha illaa anta, xolaqtaniy va ana ‘abduka, va ana ‘alaa ‘ahdika va va‘dika mastato‘tu. A‘uuzu bika min sharri maa sona‘tu. Abuu’u laka bini‘matika ‘alayya va abuu’u bizanbiy, fag‘firliy fa’innahuu laa yag‘firuz-zunuuba illaa anta.',
    uz: 'Ey Allohim, Sen mening Rabbimsan, Sendan o‘zga iloh yo‘q. Meni Sen yaratding, men Sening bandangman. Qodir bo‘lganimcha Sening ahdingda va va’dang ustidaman. Qilgan ishimning yomonligidan Senga panoh tilayman. Senga bergan ne’matingni tan olaman va gunohimni ham tan olaman. Meni mag‘firat qil, chunki gunohlarni Sendan o‘zga hech kim mag‘firat qila olmaydi.',
    fazl: 'Kim uni ishonch bilan o‘sha kuni ertalab aytsa va kech kirmay vafot etsa, jannat ahlidan bo‘ladi. Kim kechqurun ishonch bilan aytsa va tong otmay vafot etsa, u ham jannat ahlidan bo‘ladi.',
    src: 'Buxoriy 6306' };

  const ASBAH = { id: 'mulk', t: 'Asbahna va asbahal-mulk', n: 1,
    ar: 'أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، رَبِّ أَسْأَلُكَ خَيْرَ مَا فِي هَذَا الْيَوْمِ وَخَيْرَ مَا بَعْدَهُ، وَأَعُوذُ بِكَ مِنْ شَرِّ مَا فِي هَذَا الْيَوْمِ وَشَرِّ مَا بَعْدَهُ، رَبِّ أَعُوذُ بِكَ مِنَ الْكَسَلِ وَسُوءِ الْكِبَرِ، رَبِّ أَعُوذُ بِكَ مِنْ عَذَابٍ فِي النَّارِ وَعَذَابٍ فِي الْقَبْرِ',
    tr: 'Asbahnaa va asbahal-mulku lillaah, val-hamdu lillaah, laa ilaaha illallohu vahdahuu laa shariika lah, lahul-mulku va lahul-hamdu va huva ‘alaa kulli shay’in qodiir. Robbi as’aluka xoyro maa fiy haazal-yavmi va xoyro maa ba‘dah, va a‘uuzu bika min sharri maa fiy haazal-yavmi va sharri maa ba‘dah. Robbi a‘uuzu bikal-kasali va suu’il-kibar. Robbi a‘uuzu bika min ‘azaabin fin-naari va ‘azaabin fil-qobr.',
    uz: 'Tong otdi va mulk Allohnikidir, hamd Allohgadir. Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U hamma narsaga qodirdir. Ey Rabbim, bu kunning yaxshiligini va undan keyingi yaxshilikni Sendan so‘rayman. Bu kunning yomonligidan va undan keyingi yomonlikdan Senga panoh tilayman. Ey Rabbim, dangasalikdan va keksalikning yomonligidan Senga panoh tilayman. Ey Rabbim, do‘zaxdagi azobdan va qabrdagi azobdan Senga panoh tilayman.',
    fazl: 'Rasululloh ﷺ ertalab va kechqurun shu duoni aytar edilar.', src: 'Muslim 2723' };
  const AMSAY = { ...ASBAH, id: 'mulk', t: 'Amsaynaa va amsal-mulk',
    ar: 'أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، رَبِّ أَسْأَلُكَ خَيْرَ مَا فِي هَذِهِ اللَّيْلَةِ وَخَيْرَ مَا بَعْدَهَا، وَأَعُوذُ بِكَ مِنْ شَرِّ مَا فِي هَذِهِ اللَّيْلَةِ وَشَرِّ مَا بَعْدَهَا، رَبِّ أَعُوذُ بِكَ مِنَ الْكَسَلِ وَسُوءِ الْكِبَرِ، رَبِّ أَعُوذُ بِكَ مِنْ عَذَابٍ فِي النَّارِ وَعَذَابٍ فِي الْقَبْرِ',
    tr: 'Amsaynaa va amsal-mulku lillaah, val-hamdu lillaah, laa ilaaha illallohu vahdahuu laa shariika lah, lahul-mulku va lahul-hamdu va huva ‘alaa kulli shay’in qodiir. Robbi as’aluka xoyro maa fiy haazihil-laylati va xoyro maa ba‘dahaa, va a‘uuzu bika min sharri maa fiy haazihil-laylati va sharri maa ba‘dahaa. Robbi a‘uuzu bikal-kasali va suu’il-kibar. Robbi a‘uuzu bika min ‘azaabin fin-naari va ‘azaabin fil-qobr.',
    uz: 'Kech kirdi va mulk Allohnikidir, hamd Allohgadir. Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U hamma narsaga qodirdir. Ey Rabbim, bu kechaning yaxshiligini va undan keyingi yaxshilikni Sendan so‘rayman. Bu kechaning yomonligidan va undan keyingi yomonlikdan Senga panoh tilayman. Ey Rabbim, dangasalikdan va keksalikning yomonligidan Senga panoh tilayman. Ey Rabbim, do‘zaxdagi azobdan va qabrdagi azobdan Senga panoh tilayman.' };

  const BIKA_M = { id: 'bika', t: 'Allohumma bika asbahna', n: 1,
    ar: 'اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ',
    tr: 'Allohumma bika asbahnaa va bika amsaynaa va bika nahyaa va bika namuutu va ilaykan-nushuur.',
    uz: 'Ey Allohim, Sening yordaming bilan tong ottirdik, Sening yordaming bilan kech kiritdik, Sening irodang bilan yashaymiz, Sening irodang bilan vafot etamiz va qayta tirilish Senga bo‘ladi.',
    fazl: 'Rasululloh ﷺ ertalab shu duoni aytar edilar.', src: 'Termiziy 3391' };
  const BIKA_E = { ...BIKA_M, t: 'Allohumma bika amsaynaa',
    ar: 'اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ',
    tr: 'Allohumma bika amsaynaa va bika asbahnaa va bika nahyaa va bika namuutu va ilaykal-masiir.',
    uz: 'Ey Allohim, Sening yordaming bilan kech kiritdik, Sening yordaming bilan tong ottirdik, Sening irodang bilan yashaymiz, Sening irodang bilan vafot etamiz va qaytish Senga bo‘ladi.',
    fazl: 'Rasululloh ﷺ kechqurun shu duoni aytar edilar.' };

  const AFW = { id: 'afw', t: 'Afv va omonlik duosi', n: 1,
    ar: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي دِينِي وَدُنْيَايَ وَأَهْلِي وَمَالِي، اللَّهُمَّ اسْتُرْ عَوْرَاتِي وَآمِنْ رَوْعَاتِي، اللَّهُمَّ احْفَظْنِي مِنْ بَيْنِ يَدَيَّ وَمِنْ خَلْفِي وَعَنْ يَمِينِي وَعَنْ شِمَالِي وَمِنْ فَوْقِي، وَأَعُوذُ بِعَظَمَتِكَ أَنْ أُغْتَالَ مِنْ تَحْتِي',
    tr: 'Allohumma innii as’alukal-‘afva val-‘aafiyata fid-dunyaa val-aaxiroh. Allohumma innii as’alukal-‘afva val-‘aafiyata fii diiniy va dunyaaya va ahliy va maaliy. Allohummas-tur ‘avrootiy va aamin ravo‘aatiy. Allohummah-fazniy min bayni yadayya va min xolfiy va ‘an yamiiniy va ‘an shimaaliy va min fawqiy, va a‘uuzu bi‘azomatika an ug‘taala min tahtiy.',
    uz: 'Ey Allohim, Sendan dunyo va oxiratda afv va omonlik so‘rayman. Ey Allohim, dinimda, dunyoimda, oilamda va molimda afv va omonlik so‘rayman. Ey Allohim, aybimni yop va qo‘rquvlarimni omonlikka aylantir. Ey Allohim, meni oldimdan, ortimdan, o‘ng tomonimdan, chap tomonimdan va tepamdan saqla. Pastimdan to‘satdan yer yutib ketishidan Sening ulug‘ligingga panoh tilayman.',
    fazl: 'Ibn Umar roziyallohu anhu aytadi: Rasululloh ﷺ ertalab va kechqurun bu duoni tark qilmas edilar.', src: 'Abu Dovud 5074, Ibn Moja 3871' };

  const GHAYB = { id: 'ghayb', t: 'G‘oyibni biluvchi duosi', n: 1,
    ar: 'اللَّهُمَّ عَالِمَ الْغَيْبِ وَالشَّهَادَةِ فَاطِرَ السَّمَاوَاتِ وَالْأَرْضِ، رَبَّ كُلِّ شَيْءٍ وَمَلِيكَهُ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا أَنْتَ، أَعُوذُ بِكَ مِنْ شَرِّ نَفْسِي وَمِنْ شَرِّ الشَّيْطَانِ وَشِرْكِهِ',
    tr: 'Allohumma ‘aalimal-g‘oybi vash-shahaadati faatiros-samaavaati val-ard, Robba kulli shay’in va maliikah, ashhadu an laa ilaaha illaa anta, a‘uuzu bika min sharri nafsiy va min sharrish-shaytoni va shirkih.',
    uz: 'Ey Allohim, g‘oyib va oshkorani biluvchi, osmonlar va yerning yaratuvchisi, har narsaning Rabbi va egasi! Sendan o‘zga iloh yo‘qligiga guvohlik beraman. Nafsimning yomonligidan, shaytonning yomonligidan va uning shirkidan Senga panoh tilayman.',
    fazl: 'Rasululloh ﷺ Abu Bakr roziyallohu anhuga: “Buni ertalab, kechqurun va to‘shakka yotganingda ayt”, dedilar.', src: 'Abu Dovud 5067, Termiziy 3392' };

  const BISMILLAH = { id: 'bismillah', t: 'Bismillahil-lazi la yadurru', n: 3,
    ar: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ',
    tr: 'Bismillaahil-laziy laa yadurru ma‘asmihii shay’un fil-ardi va laa fis-samaa’i va huvas-samii‘ul-‘aliim.',
    uz: 'Ismi bilan yerda ham, osmonda ham hech narsa zarar yetkaza olmaydigan Alloh nomi bilan. U eshituvchi va biluvchidir.',
    fazl: 'Kim ertalab va kechqurun uch martadan shuni aytsa, unga hech narsa zarar bermaydi.', src: 'Abu Dovud 5088, Termiziy 3388' };

  const RODIYTU = { id: 'rodiytu', t: 'Rodiytu billahi Robban', n: 3,
    ar: 'رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ نَبِيًّا',
    tr: 'Rodiytu billaahi Robban, va bil-islaami diinan, va bi-Muhammadin nabiyyan.',
    uz: 'Alloh Rabb, Islom din va Muhammad ﷺ payg‘ambar bo‘lganidan rozi bo‘ldim.',
    fazl: 'Kim ertalab va kechqurun uch martadan shuni aytsa, qiyomat kuni uni rozi qilish Allohning zimmasidagi haqdir.', src: 'Abu Dovud 5072, Termiziy 3389' };

  const TASBEH = { id: 'tasbeh', t: 'Subhanallohi va bihamdih', n: 100,
    ar: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ', tr: 'Subhaanallohi va bihamdih.',
    uz: 'Allohni barcha nuqsonlardan poklayman va Unga hamd aytaman.',
    fazl: 'Kim kuniga yuz marta shuni aytsa, gunohlari dengiz ko‘pigicha bo‘lsa ham kechiriladi.', src: 'Buxoriy 6405, Muslim 2691' };

  const TAHLIL = { id: 'tahlil', t: 'La ilaha illalloh', n: 100,
    ar: 'لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ',
    tr: 'Laa ilaaha illallohu vahdahuu laa shariika lah, lahul-mulku va lahul-hamdu va huva ‘alaa kulli shay’in qodiir.',
    uz: 'Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U hamma narsaga qodirdir.',
    fazl: 'Kim kuniga yuz marta shuni aytsa, unga o‘nta qul ozod qilgan savobi bo‘ladi, yuzta yaxshilik yoziladi, yuzta yomonligi o‘chiriladi va o‘sha kuni kechgacha shaytondan himoyada bo‘ladi.', src: 'Buxoriy 3293, Muslim 2691' };

  const JUWAYRIYA = { id: 'adada', t: 'Subhanallohi ‘adada xolqih', n: 3,
    ar: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ',
    tr: 'Subhaanallohi va bihamdihii ‘adada xolqih, va ridoo nafsih, va zinata ‘arshih, va midaada kalimaatih.',
    uz: 'Allohni poklayman va Unga hamd aytaman: Uning maxluqotlari sonicha, O‘zi rozi bo‘ladigan miqdorda, Arshining og‘irligicha va kalimalari siyohicha.',
    fazl: 'Rasululloh ﷺ Juvayriya roziyallohu anhoga: “Sendan keyin to‘rt kalimani uch marta aytdim. Sen bugun aytganlaring bilan tortilsa, ular og‘irroq keladi”, dedilar.', src: 'Muslim 2726' };

  const AUZU = { id: 'auzu', t: 'A‘uzu bikalimatillahit-tammat', n: 3,
    ar: 'أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ',
    tr: 'A‘uuzu bikalimaatillaahit-taammaati min sharri maa xolaq.',
    uz: 'Alloh yaratgan narsalarning yomonligidan Allohning komil kalimalari bilan panoh tilayman.',
    fazl: 'Kim kechqurun uch marta shuni aytsa, o‘sha kecha unga zahar zarar bermaydi.', src: 'Termiziy 3604' };

  window.ZIKR_DATA = {
    morning: [KURSI, IKHLOS, FALAQ, NOS, SAYYID, ASBAH, BIKA_M, AFW, GHAYB, BISMILLAH, RODIYTU, TASBEH, TAHLIL, JUWAYRIYA],
    evening: [KURSI, IKHLOS, FALAQ, NOS, SAYYID, AMSAY, BIKA_E, AFW, GHAYB, BISMILLAH, RODIYTU, TASBEH, TAHLIL, AUZU],
  };
})();
