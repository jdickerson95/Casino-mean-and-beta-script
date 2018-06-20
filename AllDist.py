import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    '''
    DISTRIBUTIONS = [
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]
    '''
    DISTRIBUTIONS = [st.genlogistic, st.gamma, st.gumbel_r, st.gumbel_l,st.johnsonsb, st.johnsonsu, st.norm, st.uniform
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params, best_distribution)

def make_pdf(data, distribution, params,):
    """Generate distributions's Propbability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]


    # Build PDF and turn into pandas Series
    x = np.linspace(data[0], data[len(data) - 1], 1000)
    y = distribution.pdf(x, loc=loc, scale=scale, *arg)
 #   pdf = pd.Series(y, x)

    return y

def getData(set):
    f = open('intDataPoints.txt', 'r')
    dataSet = []
    weights = []
    for line in f:
        wholeLine = line.strip().split()
        dataSet.append([float(wholeLine[set]), float(wholeLine[2])])
        weights.append(float(wholeLine[2]))
    dataSet = sorted(dataSet,key=lambda x: (x[0],x[1]))
    totWeight = sum(weights)
    runningWeight = 0.
    new = True
    startVal = dataSet[0][0]
    setVals = []
    for x in range(len(dataSet)):
        runningWeight += dataSet[x][1]
        if runningWeight >= totWeight/100:
            setVals.append((dataSet[x][0] + startVal)/2)
            runningWeight -= (totWeight/100)
            startVal = dataSet[x][0]

    return setVals

# Load data from statsmodels datasets
def loop():
    for i in range(2):
        data = getData(i)
        x = np.linspace(data[0], data[len(data) - 1], 1000)
        # Plot for comparison
    #    plt.figure(1, figsize=(12,8))
    #   ax = data.plot(kind='hist', bins=10, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
        # Save plot limits
    #  dataYLim = ax.get_ylim()

        # Find best fit distribution
        best_fit_name, best_fir_paramms, distribution = best_fit_distribution(data, 200, None)
        best_dist = getattr(st, best_fit_name)

        # Update plots
    #   ax.set_ylim(dataYLim)
    #  ax.set_xlabel('mH0')

        #Make PDF
        pdf = make_pdf(data, distribution, best_fir_paramms)

        # Display
        plt.figure(i, figsize=(12,8))
        plt.hist(data, 10, normed=1)

        param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
        param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fir_paramms)])
        dist_str = '{}({})'.format(best_fit_name, param_str)
        blue_line, = plt.plot(x, pdf, color='b', label=best_fit_name)
        plt.legend(handles=[blue_line])
        plt.xlabel('mH' + str(i))
        plt.title(dist_str)
    plt.show()
if __name__ == "__main__":
    loop()