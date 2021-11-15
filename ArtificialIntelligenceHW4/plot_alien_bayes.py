from matplotlib import pyplot as plt
import alien_bayes


def two_line_plot(xvals1, yvals1, label1, xvals2, yvals2, label2, title, outfile_path):
    plt.plot(xvals1, yvals1, label=label1, color='blue', marker='.', linestyle='solid')
    plt.plot(xvals2, yvals2, label=label2, color='green', marker='.', linestyle='solid')
    plt.title(title)
    plt.legend()
    plt.savefig(outfile_path)

nodes = alien_bayes.ALIEN_NODES
n = 100
f = 200
query = { 'A': True, 'M': True , 'B': True}
for i in range(n,f):

    reject_prob = alien_bayes.RejectionSampler(nodes).get_prob(query,{}, i)
    weight_prob = alien_bayes.LikelihoodWeightingSampler(nodes).get_prob(query,{}, i)
    samples_reject = alien_bayes.RejectionSampler(nodes).generate_samples(i,{})
    samples_weight = alien_bayes.LikelihoodWeightingSampler(nodes).generate_samples(i,{})

    two_line_plot(len(samples_reject), reject_prob, "Rejection Sampling", len(samples_weight), weight_prob, "Likelihood weighting", "P(abduct | memory, burning)","alien_bayes.pdf")

# reject_prob = alien_bayes.RejectionSampler(nodes).get_prob(query,{}, n)
# weight_prob = alien_bayes.LikelihoodWeightingSampler(nodes).get_prob(query,{}, n)
# samples_reject = alien_bayes.RejectionSampler(nodes).generate_samples(n,{})
# samples_weight = alien_bayes.LikelihoodWeightingSampler(nodes).generate_samples(n,{})
#
#
# two_line_plot(len(samples_reject), reject_prob, "Rejection Sampling", len(samples_weight), weight_prob, "Likelihood weighting", "P(abduct | memory, burning)","alien_bayes.pdf")


# two_line_plot(n, reject_prob, "Rejection Sampling", n, weight_prob, "Likelihood weighting", "P(abduct | memory, burning)","alien_bayes.pdf")
#
# Fill in this script to empirically calculate P(A=true | M=true, B=true) using the rejection
# sampling and likelihood weighting code found in alien_bayes.py.
#
# Use the two_line_plot() function above to generate a line graph with one line for each
# approximation technique.  The x-axis should represent different n, the number of samples
# generated, with the probability estimate for the conditional probability above on the y-axis.
#
# You should generate estimates using at least 100 different values of n, and increase it to
# the point that the estimates appear to stabilize.  Note that for rejectins sampling, n should
# represent the number of simple samples created, not the number retained after rejecting those
# that do not agree with the evidence.
#
# Your script should produce a plot named "alien_bayes.pdf".
#
