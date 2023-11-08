#!/usr/bin/env python
# Unravel the nested dictionaries into flat files

import pandas as pd

# EF Group
import efgroup2ef
ef2ef = pd.DataFrame.from_dict(efgroup2ef.EF_GROUP_2_EF, orient='index')
ef2ef['efgroup'] = ef2ef.index
ef2ef = pd.melt(ef2ef, id_vars='efgroup', var_name='species', value_name='ef')
ef2ef.sort_values(['efgroup','species'], inplace=True)
ef2ef[ef2ef.ef.notnull()].to_csv('efgroup2ef.csv', index=False)

import catphase2efgroup
cdict = catphase2efgroup.CAT_PHASE_2_EF_GROUP
# {efgroup: {fuelclass: {fuel: {phase: {species: ef
cat2ef = pd.DataFrame.from_dict({(i,j,k,l): cdict[i][j][k][l] for i in cdict.keys() for j in cdict[i].keys() for k in cdict[i][j].keys() for l in cdict[i][j][k].keys()}, orient='index')
idcols = ['regefgroup','fuelcat','fuelsubcat','phase']
cat2ef.reset_index(names=idcols, inplace=True)
cat2ef = pd.melt(cat2ef, id_vars=idcols, var_name='species', value_name='efgroup')
cat2ef[cat2ef.efgroup.notnull()].to_csv('catphase2efgroup.csv', index=False)

import covertype2efgroupname
c2ef = pd.DataFrame.from_dict(covertype2efgroupname.COVERTYPE_2_EF_GROUP_NAME, orient='index')
c2ef.columns = ['efgroupname',]
c2ef['cover'] = c2ef.index
c2ef.sort_values('cover', inplace=True)
c2ef.to_csv('covertype2efgroupname.csv', index=False, columns=['cover','efgroupname'])

import covertype2efgroup
c2ef = pd.DataFrame.from_dict(covertype2efgroup.COVERTYPE_2_EF_GROUP, orient='index')
c2ef['cover'] = c2ef.index
c2ef = pd.melt(c2ef, id_vars='cover', var_name='phase', value_name='efgroup')
c2ef.sort_values(['cover','phase'], inplace=True)
c2ef.to_csv('covertype2efgroup.csv', index=False)


import efgroupname2seraef
cdict = efgroupname2seraef.EF_GROUP_NAME_2_SERA_EF
# {region: {efgroupname: {phase: {species: {stat: val
ef2sera = pd.DataFrame.from_dict({(i,j,k,l): cdict[i][j][k][l] for i in cdict.keys() for j in cdict[i].keys() for k in cdict[i][j].keys() for l in cdict[i][j][k].keys()}, orient='index')
idcols = ['region','efgroupname','phase','species']
ef2sera.reset_index(names=idcols, inplace=True)
ef2sera.to_csv('efgroupname2seraef.csv', index=False)

import fccs2covertype
f2ct = pd.DataFrame.from_dict(fccs2covertype.FCCS_2_COVERTYPE, orient='index')
f2ct.columns = ['cover',]
f2ct['fccs_id'] = f2ct.index
f2ct.sort_values('fccs_id', inplace=True)
f2ct.to_csv('fccs2covertype.csv', index=False, columns=['fccs_id','cover'])

import fuelcategory2seraphaseexceptions
cdict = fuelcategory2seraphaseexceptions.FUEL_CATEGORY_2_SERA_PHASE_EXCEPTIONS
# {fuelcat: {fuelsubcat: {phase: exception
f2sp = pd.DataFrame.from_dict({(i,j): cdict[i][j] for i in cdict.keys() for j in cdict[i].keys()}, orient='index')
idcols = ['fuelcat','fuelsubcat']
f2sp.reset_index(names=idcols, inplace=True)
f2sp = pd.melt(f2sp, id_vars=idcols, var_name='phase', value_name='exception')
f2sp.to_csv('fuelcategory2seraphaseexceptions.csv', index=False)

