hype_filter = ['manoo', 'manooooooo', 'pogggg', 'manooooo', 'manooooooooooooo', 'f', 'tapohaaaaaaa', 'mdsssssss', 'caralhoo', 
               'wtff', 'manoooooooo', 'ta porraaaaa', 'manooooooooooo', 'mdsssss', 'poggeers', 'pogg', 'eiitaaa', 'mdssss', 
               'manoooo', 'nemmm', 'pogggggggg', 'MEU DEUS', 'tapohaaaa', 'mdsss', 'tapooha', 'nemm', 'pog champ', 'pog champp',
                 'TAPOOOORRAAAAA', 'eiita', 'mdssssss', 'wtffff', 'remakeee', 'tapohaaaaa', 'wtfff', 'caralhoooo', 
                 'manoooooooooooo', 'Lkkkknoooo', 'eiiitaa', 'pogggggg', 'manoooooo', 'tapohaaa', 'poggggg', 'manooo', 
                 'caralhooooooo', 'ta porraaaa', 'eitaaaaa', 'ele sabe de algo', 'eitaa', 'poggers', 'kekw mano', 
                 'ta porraaaaaa', 'tapoooha', 'omegalull', 'eita', 'OMEGALUL', 'NEM', 'neeem', 'caralhooo', 'RMK', 
                 'tapohaaaaaa', 'CARALHOOOOOOO', 'mano', 'pooggggg', 'taapoohaaaaaa', 'NEM FUDENDO MANO VSFDPQP', 
                 'omegalulll', 'poogggggg', 'manoooooooooo', 'manooooooooo', 'eitaaa', 'mdss', 'pog', 'remake', 'poggg', 
                 'caralhooooo', 'caralhoooooooo', 'ta porraaa', 'caralhoooooo', 'MDS']
                  #Enphase words from a normal Brazilian twich chat and its variations

#Capitalize
hype_filter_capitalize = [s.capitalize() for s in hype_filter]

#Lower
hype_filter_lower = [s.lower() for s in hype_filter]

#Capitalize + Lower
hype_filter_lower.extend(hype_filter_capitalize)

#Upper
hype_filter_upper = [s.upper() for s in hype_filter]