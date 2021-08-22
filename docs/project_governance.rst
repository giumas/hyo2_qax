.. _project-governance:

Project Governance
==================

This document describes how the QAX Project is managed. The primary topics are:

* The membership of the **QAX Steering Committee**.
* The decision process related to **QAX Project changes**.
* The handling of **code changes**.

In brief, the QAX Steering Committee votes on proposals created as
`GitHub tickets <https://github.com/ausseabed/qax/issues>`_.
These proposals are available for review for at least three business days.
A single veto is sufficient to delay proposal acceptance although ultimately
a majority of members can pass a proposal.
All not-minor code changes require at least 1 reviewer.

Steering Committee
------------------

#. The current committee membership list is made available on the QAX GitHub repository.
#. The Chair is responsible for keeping track of who is a member of the Project Management Committee.
#. Addition and removal of members from the committee, as well as selection of a new Chair should be handled as
   a proposal to the committee.
#. The Steering Committee votes on proposals and decides the allowed reviewers of
   `GitHub pull requests <https://github.com/ausseabed/qax/pulls>`_.

Decision Process
----------------

#. A proposal is created as a `GitHub ticket <https://github.com/ausseabed/qax/issues>`_
   for discussion and voting by any interested party (not just the committee members).
#. Before a final decision can be made, a proposal needs to be available for review for (at least) three business days.
#. Respondents may vote:

   * "+1" to indicate support for the proposal (and a willingness to support implementation).
   * "+0" to indicate mild support, but has no effect.
   * "0" in case of no opinion.
   * "-0" to indicate mild disagreement, but has no effect.
   * "-1" to veto a proposal, but **must** be provided clear reasoning and/or an alternate approach to resolve the issue.

#. Anyone may comment on a proposal, but only members of the QAX Steering Committee’s votes will be counted.
   The Committee Chair gets a vote too.

#. A proposal is accepted if it receives at least +2 (including the proposer) and no vetos ('-1').

#. After that a proposal has been available for (at least) three business day, the proposer announces whether
   the proposal was accepted or vetoed based on the counted votes. The proposer notes the outcome on
   the `GitHub ticket <https://github.com/ausseabed/qax/issues>`_.

#. In case that a proposal is vetoed and cannot be revised to satisfy all parties, a proposal can be resubmitted
   for a *majority vote*.

   * In such a case, it is sufficient that it gets a majority of '+1' from all committee members
     (not just from those who actively voted).
   * In case of a tie, the decision on the proposal is taken by the Committee Chair.
   * The majority vote can be used to override an obstructionist veto, but it is intended that in normal circumstances
vetoers need to be convinced to withdraw their veto. We are trying to reach consensus.

When is a Proposal Required?
----------------------------

Anything that might be controversial. For instance:

* When a relevant release should take place (not required for bug-fix releases).
* Adding a substantial amount of new code.
* Changes that breaks backward compatibility.

Code Changes
------------

Whether or not a proposal is required, all not-minor code changes require the submission of
a `GitHub pull request <https://github.com/ausseabed/qax/pulls>`_.

Before a proposal is merged, at least 1 reviewer (different than the submitter) needs to approve
the code changes.

Bootstrapping
-------------

Lachlan Hurst (FrontiersSI), Xxxx Yyyyyy (Geoscience Australia), Zzzz Wwwww (Kkkkk), Tyanne Faulkes (NOAA, OCS) and
Giuseppe Masetti (UNH, CCOM) are declared to be the founding QAX Steering Committee.

Lachlan Hurst is declared initial Chair of the QAX Steering Committee.
