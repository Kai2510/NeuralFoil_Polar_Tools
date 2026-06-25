import neuralfoil as nf  # `pip install neuralfoil`
import aerosandbox as asb  # `pip install aerosandbox`
import numpy as np

foil_name = 'JX-RS-Root'
# foil_name = 'TL54m3-h7-m1-h75-m0.5-h85-m1.5-r0.8'
# foil_name = 'E-N-2575'
# foil_name = 'E63'
# foil_name = 'NACA4412'

dat_path="E:/Program Files/Aero/FlyingWing/Amokka-JX/CAD/Profile für SWX/JX-RS/"+ foil_name +".dat"
# dat_path="E:/Program Files/Aero/FlyingWing/"+ foil_name +".dat"
Re = 30000
Alpha_Low = -20
Alpha_High = 20
Alpha_step = 0.5
# Re_list = [30000,50000,70000,90000,120000,150000,180000,220000,250000,300000,400000]
Re_list = [50000,100000,200000,300000,400000,600000,800000]

for Re in Re_list:
    output_file_name = "./NeuralFoil_Data/"+foil_name + "_Re"+ str(format(Re/1e6,'.3f')) +'.txt'

    with open(output_file_name,'w') as f:
        f.writelines(["Neuralfoil\n","\n","Calculated polar for: "+foil_name+"\n","\n","Re = "+str(Re)+"\n","\n","\n","\n","\n","alpha\tCL\tCD\tCm\tTop Xtr\tBot Xtr\n"])
        for Alpha in np.arange(Alpha_Low,Alpha_High+Alpha_step,Alpha_step):
            aero = nf.get_aero_from_dat_file(  # You can use a .dat file as an entry point
                filename = dat_path,
                alpha=Alpha,  # Angle of attack [deg]
                Re=Re,  # Reynolds number [-]
                model_size="xxxlarge",  # Optionally, specify your model size.
            )
            f.writelines(str(Alpha)+"\t"+str(aero["CL"][0])+"\t"+str(aero["CD"][0])+"\t"+str(aero["CM"][0])+"\t"+str(aero["Top_Xtr"][0])+"\t"+str(aero["Bot_Xtr"][0])+"\n")



# output_file_name = "./NeuralFoil_Data/"+foil_name + "_Re"+ str(Re/1000000) +'.txt'
#
# with open(output_file_name,'w') as f:
#     f.writelines(["Neuralfoil\n","\n","Calculated polar for: "+foil_name+"\n","\n","Re = "+str(Re)+"\n","\n","\n","\n","\n","Alpha\tCL\tCD\tCM\tTop_Xtr\tBot_Xtr\n"])
#     for Alpha in np.arange(Alpha_Low,Alpha_High+Alpha_step,Alpha_step):
#         aero = nf.get_aero_from_dat_file(  # You can use a .dat file as an entry point
#             filename = dat_path,
#             alpha=0,  # Angle of attack [deg]
#             Re=5e6,  # Reynolds number [-]
#             model_size="xxxlarge",  # Optionally, specify your model size.
#         )
#         f.writelines(str(Alpha)+"\t"+str(aero["CL"][0])+"\t"+str(aero["CD"][0])+"\t"+str(aero["CM"][0])+"\t"+str(aero["Top_Xtr"][0])+"\t"+str(aero["Bot_Xtr"][0])+"\n")


# aero = nf.get_aero_from_airfoil(  # You can use AeroSandbox airfoils as an entry point
#     airfoil=asb.Airfoil("naca4412"),  # any UIUC or NACA airfoil name works
#     alpha=5, Re=5e6,
# )
# print(aero["CL"][0],aero["CM"]);
#
# # aero = nf.get_aero_from_coordinates(  # You can use xy airfoil coordinates as an entry point
# #     coordinates=n_by_2_numpy_ndarray_of_airfoil_coordinates,
# #     alpha=np.linspace(-25, 25, 1000),  # Vectorize your evaluations across `alpha` and `Re`
# #     Re=5e6,
# # )




# `aero` is a dictionary with keys: ["analysis_confidence", "CL", "CD", "CM", "Top_Xtr", "Bot_Xtr", ...]
