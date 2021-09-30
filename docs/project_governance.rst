.. _project-governance:

Project Governance
==================

This document describes how the QAX Project is managed. The primary topics are:

* QAX Steering Committee
    * Role
    * Membership
    * Meetings
* Project work
    * Definition and process
    * Decision process
    * Ad Hoc Meetings
    * Quality control
    * Risk management
    * Problem Resolution
    * Communications
    * Principles of collaboration


Steering Committee
------------------
Roles
^^^^^
The Steering Committee:

* Oversees the management and direction of the QAX project
* Votes on proposals created as GitHub tickets
* Manages roles within the GitHub repository (e.g. reviewer, owner, etc)
* Will elect a Chair from the committee
* Are responsible for communicating project intentions to the broader community

Chair:

* Responsible for leading and organizing meetings
* Managing GitHub membership and roles
* Monitoring actions arising from committee meetings
* Maintain decision registry
* Will retain the role for 1 year (??)
* Is elected annually by the Steering Committee (??)


Bootstrapping
^^^^^^^^^^^^^

Lachlan Hurst (FrontiersSI), Justy Siwabessy (Geoscience Australia), Zzzz Wwwww (Kkkkk), Tyanne Faulkes (NOAA, OCS) and
Giuseppe Masetti (UNH, CCOM) are declared to be the founding QAX Steering Committee.

Lachlan Hurst is declared initial Chair of the QAX Steering Committee.


Membership
^^^^^^^^^^

The current committee membership list is made available on the QAX GitHub repository.

Addition and removal of members from the steering committee, as well as nomination of a new Chair
should be handled as a proposal to the committee.


Meetings
^^^^^^^^
Frequency
"""""""""
Meetings will be held on a quarterly basis at a minimum and where needed intersessional meetings can be held.


Content and Preparation
"""""""""""""""""""""""
A quarterly meeting will be scheduled two months in advance; with the agenda and associated material
distributed one week ahead of the meeting.

Meeting could include the following topics:

* Last quarter's progress
* Risk and issue management
* Plan and intentions for upcoming quarter
* Proposal review and voting, where appropriate
* Establish roles for successful proposal implementation


Record keeping
""""""""""""""

Responsibility for minute taking and distribution post-meeting will rotate between SC members.

Decision registry will be maintained by the Chair and stored in the shared space.

Documentation will be published on the `wiki associated with this repository <https://github.com/ausseabed/qax/wiki>`_. (??)

#. The current committee membership list is made available on the QAX GitHub repository.
#. The Chair is responsible for keeping track of who is a member of the Project Management Committee.
#. Addition and removal of members from the committee, as well as selection of a new Chair should be handled as
   a proposal to the committee.
#. The Steering Committee votes on proposals and decides the allowed reviewers of
   `GitHub pull requests <https://github.com/ausseabed/qax/pulls>`_.


Project Work
------------

Definition and process
^^^^^^^^^^^^^^^^^^^^^^

A proposal can be classified into two categories: minor and major proposals.

Some examples of minor proposals are:

* Updates to Documentation
* Bug fixes

Some examples of major proposals are:

* Any change involving a significant amount of new code
* Changes that break backward compatibility


Process
^^^^^^^

The following process is to be undertaken for all major proposals.

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
   the `GitHub issue <https://github.com/ausseabed/qax/issues>`_.

#. If a proposal is vetoed and cannot be revised to satisfy all parties, a proposer can request a *majority vote*.

   Majority vote is a mechanism to override an obstructing veto. However, it is the intention of the QAX
   collaborators that the SC should always strive to reach a consensus and that a majority vote should only be
   enacted once all other resolution options are exhausted, and the SC reach an impasse.

   * If a majority vote is called the proposer and the vetoer must both make their case before the SC.
   * All SC members must vote (using any score options outlined above). For a proposal to pass a majority
     vote it must receive a total score of at least +1.
   * In case of a tie (final score is 0), the decision on the proposal is taken by the Committee Chair.
   * The majority vote can be used to override an obstructionist veto, but it is intended that in normal circumstances
     vetoers need to be convinced to withdraw their veto. We are trying to reach consensus.


Ad Hoc Meetings
^^^^^^^^^^^^^^^

Ad Hoc meetings can be called by any SC member and do not need to contain the full complement of QSC
members. These meetings are to be held to facilitate project work and activities.

At a minimum actions and notes should be emailed to SC following an ad hoc meeting and stored in the
`wiki associated with this repository <https://github.com/ausseabed/qax/wiki>`_ (??).


Quality Control
^^^^^^^^^^^^^^^

Whether or not a proposal is required, all non-minor code changes require the submission of
a `GitHub pull request <https://github.com/ausseabed/qax/pulls>`_.

Before a proposal is merged, at least 1 reviewer (different than the submitter) needs to approve
the code changes.


Risk management
^^^^^^^^^^^^^^^

Major proposals need to identify risks associated with work and implement management strategies.


Communications and Outreach
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any activity that has the potential to generate public interest should be discussed as an outreach
opportunity during the proposal phase.

Where SC agree that public communication is required, the proposer should generate a communication
plan for the SC to review.

Any articles or posts mentioning the SC organisations will require sign-off from each organisation
mentioned and sufficient lead time will be given to meet internal processes.


Principles of collaboration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is in the best interest to communicate early and clearly to avoid conflict and undue tensions.
Should issues begin to arise from email communication, collaborators should move quickly to hold
a virtual face-to-face meeting to align understanding.

Should issues persist or the situation warrant it, a third-party mediator could be invited to
assist with discussions.