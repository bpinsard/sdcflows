# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""Build a dataset-wide estimation workflow."""


def init_sdcflows_wf():
    """Create a multi-subject, multi-estimator *SDCFlows* workflow."""
    from nipype.pipeline.engine import Workflow
    from niworkflows.utils.bids import collect_participants

    from sdcflows import config
    from sdcflows.utils.wrangler import find_estimators

    # Create parent workflow
    workflow = Workflow(name="sdcflows_wf")
    workflow.base_dir = config.execution.work_dir

    subjects = collect_participants(
        config.execution.layout,
        config.execution.participant_label,
    )
    estimators_record = {}
    for subject in subjects:
        estimators_record[subject] = find_estimators(
            layout=config.execution.layout,
            subject=subject,
            fmapless=config.workflow.fmapless,
            logger=config.loggers.cli,
        )

    for subject, sub_estimators in estimators_record.items():
        for estim in sub_estimators:
            workflow.add_nodes([estim.get_workflow()])

    return workflow
