#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _cad_reg(void);
extern void _cagk_reg(void);
extern void _calH_reg(void);
extern void _cal_reg(void);
extern void _car_reg(void);
extern void _cat_reg(void);
extern void _d3_reg(void);
extern void _h_reg(void);
extern void _kadist_reg(void);
extern void _kaprox_reg(void);
extern void _kca_reg(void);
extern void _kdr_reg(void);
extern void _km_reg(void);
extern void _na3dend_reg(void);
extern void _na3_reg(void);
extern void _na3notrunk_reg(void);
extern void _nap_reg(void);
extern void _nax_reg(void);
extern void _somacar_reg(void);
extern void _vmax_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"cad.mod\"");
    fprintf(stderr," \"cagk.mod\"");
    fprintf(stderr," \"calH.mod\"");
    fprintf(stderr," \"cal.mod\"");
    fprintf(stderr," \"car.mod\"");
    fprintf(stderr," \"cat.mod\"");
    fprintf(stderr," \"d3.mod\"");
    fprintf(stderr," \"h.mod\"");
    fprintf(stderr," \"kadist.mod\"");
    fprintf(stderr," \"kaprox.mod\"");
    fprintf(stderr," \"kca.mod\"");
    fprintf(stderr," \"kdr.mod\"");
    fprintf(stderr," \"km.mod\"");
    fprintf(stderr," \"na3dend.mod\"");
    fprintf(stderr," \"na3.mod\"");
    fprintf(stderr," \"na3notrunk.mod\"");
    fprintf(stderr," \"nap.mod\"");
    fprintf(stderr," \"nax.mod\"");
    fprintf(stderr," \"somacar.mod\"");
    fprintf(stderr," \"vmax.mod\"");
    fprintf(stderr, "\n");
  }
  _cad_reg();
  _cagk_reg();
  _calH_reg();
  _cal_reg();
  _car_reg();
  _cat_reg();
  _d3_reg();
  _h_reg();
  _kadist_reg();
  _kaprox_reg();
  _kca_reg();
  _kdr_reg();
  _km_reg();
  _na3dend_reg();
  _na3_reg();
  _na3notrunk_reg();
  _nap_reg();
  _nax_reg();
  _somacar_reg();
  _vmax_reg();
}
