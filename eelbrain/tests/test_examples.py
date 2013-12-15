# generated by eelbrain/scripts/make_example_tests.py
import os

from matplotlib import pyplot as plt

from eelbrain.lab import plot

dir_ = os.path.dirname(__file__)
examples_dir = os.path.join(dir_, '..', '..', 'examples')
examples_dir = os.path.abspath(examples_dir)


def test_0():
    "Test datasets/align.py"
    path = os.path.join(examples_dir, 'datasets')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('align.py')
    plt.close('all')

def test_1():
    "Test fmtxt/table.py"
    path = os.path.join(examples_dir, 'fmtxt')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('table.py')
    plt.close('all')

def test_2():
    "Test fmtxt/table_pdf.py"
    path = os.path.join(examples_dir, 'fmtxt')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('table_pdf.py')
    plt.close('all')

def test_3():
    "Test meg/mne_sample_loader.py"
    path = os.path.join(examples_dir, 'meg')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('mne_sample_loader.py')
    plt.close('all')

def test_4():
    "Test meg/simple meg.py"
    path = os.path.join(examples_dir, 'meg')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('simple meg.py')
    plt.close('all')

def test_5():
    "Test ndvar/topo.py"
    path = os.path.join(examples_dir, 'ndvar')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('topo.py')
    plt.close('all')

def test_6():
    "Test ndvar/uts cluster permutation test.py"
    path = os.path.join(examples_dir, 'ndvar')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('uts cluster permutation test.py')
    plt.close('all')

def test_7():
    "Test ndvar/uts.py"
    path = os.path.join(examples_dir, 'ndvar')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('uts.py')
    plt.close('all')

def test_8():
    "Test statistics/ANCOVA_Crawley.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('ANCOVA_Crawley.py')
    plt.close('all')

def test_9():
    "Test statistics/ANCOVA_rutherford.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('ANCOVA_rutherford.py')
    plt.close('all')

def test_10():
    "Test statistics/ANOVA.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('ANOVA.py')
    plt.close('all')

def test_11():
    "Test statistics/ANOVA_rutherford_1.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('ANOVA_rutherford_1.py')
    plt.close('all')

def test_12():
    "Test statistics/ANOVA_rutherford_2.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('ANOVA_rutherford_2.py')
    plt.close('all')

def test_13():
    "Test statistics/Fox_Prestige.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('Fox_Prestige.py')
    plt.close('all')

def test_14():
    "Test statistics/pdf.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('pdf.py')
    plt.close('all')

def test_15():
    "Test statistics/simple.py"
    path = os.path.join(examples_dir, 'statistics')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('simple.py')
    plt.close('all')

def test_16():
    "Test ui/progress_monitor.py"
    path = os.path.join(examples_dir, 'ui')
    os.chdir(path)
    plot.configure_backend(False, False)
    execfile('progress_monitor.py')
    plt.close('all')