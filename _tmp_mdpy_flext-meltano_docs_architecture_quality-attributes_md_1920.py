# from flext-meltano_docs/architecture/quality-attributes.md:1920
from __future__ import annotations


class DisasterRecoveryManager:
    """Comprehensive disaster recovery management."""

    def __init__(self, backup_manager, failover_manager, communication_manager):
        self.backup_manager = backup_manager
        self.failover_manager = failover_manager
        self.communication_manager = communication_manager
        self.dr_plans = self._load_dr_plans()

    def execute_disaster_recovery(
        self, disaster_type: str, affected_components: t.StringList
    ) -> DRResult:
        """Execute disaster recovery plan."""
        # Identify applicable DR plan
        dr_plan = self._select_dr_plan(disaster_type, affected_components)

        if not dr_plan:
            return DRResult(
                success=False,
                error=f"No DR plan found for disaster type: {disaster_type}",
            )

        # Execute DR plan phases
        recovery_result = DRResult(disaster_type=disaster_type)

        try:
            # Phase 1: Assessment
            assessment = self._execute_assessment_phase(dr_plan, affected_components)
            recovery_result.assessment = assessment

            # Phase 2: Containment
            containment = self._execute_containment_phase(dr_plan, assessment)
            recovery_result.containment = containment

            # Phase 3: Recovery
            recovery = self._execute_recovery_phase(dr_plan, containment)
            recovery_result.recovery = recovery

            # Phase 4: Restoration
            restoration = self._execute_restoration_phase(dr_plan, recovery)
            recovery_result.restoration = restoration

            recovery_result.success = True
            recovery_result.total_downtime = self._calculate_downtime(
                assessment.start_time, restoration.end_time
            )

        except Exception as e:
            recovery_result.success = False
            recovery_result.error = str(e)

        # Send notifications
        self._send_dr_notifications(recovery_result)

        return recovery_result

    def _select_dr_plan(
        self, disaster_type: str, affected_components: t.StringList
    ) -> Optional[DRPlan]:
        """Select appropriate DR plan based on disaster characteristics."""
        # Find plans that match the disaster type
        matching_plans = [
            plan
            for plan in self.dr_plans
            if plan.disaster_type == disaster_type or plan.disaster_type == "general"
        ]

        if not matching_plans:
            return None

        # Select plan with highest component coverage
        best_plan = max(
            matching_plans,
            key=lambda plan: self._calculate_coverage(plan, affected_components),
        )

        return best_plan

    def _execute_assessment_phase(
        self, dr_plan: DRPlan, affected_components: t.StringList
    ) -> AssessmentResult:
        """Execute disaster assessment phase."""
        assessment_start = datetime.utcnow()

        # Assess impact
        impact_assessment = self._assess_impact(affected_components)

        # Determine recovery priority
        priority_order = self._determine_recovery_priority(dr_plan, impact_assessment)

        # Gather forensic data
        forensic_data = self._gather_forensic_data(affected_components)

        return AssessmentResult(
            start_time=assessment_start,
            end_time=datetime.utcnow(),
            impact_assessment=impact_assessment,
            priority_order=priority_order,
            forensic_data=forensic_data,
        )

    def _execute_recovery_phase(
        self, dr_plan: DRPlan, containment_result
    ) -> RecoveryResult:
        """Execute recovery phase according to DR plan."""
        recovery_start = datetime.utcnow()
        recovery_steps = []

        for step in dr_plan.recovery_steps:
            try:
                # Execute recovery step
                step_result = self._execute_recovery_step(step)
                recovery_steps.append(step_result)

                # Check if step failed critically
                if step.critical and not step_result.success:
                    break

            except Exception as e:
                recovery_steps.append(
                    RecoveryStepResult(
                        step_name=step.name,
                        success=False,
                        error=str(e),
                        execution_time=datetime.utcnow() - recovery_start,
                    )
                )
                break

        return RecoveryResult(
            start_time=recovery_start,
            end_time=datetime.utcnow(),
            steps=recovery_steps,
            overall_success=all(step.success for step in recovery_steps),
        )

    def test_disaster_recovery(self) -> DRTestResult:
        """Test disaster recovery procedures without actual disaster."""
        test_result = DRTestResult(test_start_time=datetime.utcnow())

        for dr_plan in self.dr_plans:
            plan_test = DRPlanTest(plan_name=dr_plan.name)

            try:
                # Test plan validation
                validation_result = self._validate_dr_plan(dr_plan)
                plan_test.validation = validation_result

                # Test backup restoration
                backup_test = self._test_backup_restoration(dr_plan)
                plan_test.backup_test = backup_test

                # Test failover procedures
                failover_test = self._test_failover_procedures(dr_plan)
                plan_test.failover_test = failover_test

                # Test communication procedures
                comm_test = self._test_communication_procedures(dr_plan)
                plan_test.communication_test = comm_test

                # Overall plan test result
                plan_test.success = all([
                    validation_result.success,
                    backup_test.success,
                    failover_test.success,
                    comm_test.success,
                ])

            except Exception as e:
                plan_test.success = False
                plan_test.error = str(e)

            test_result.plan_tests.append(plan_test)

        test_result.test_end_time = datetime.utcnow()
        test_result.overall_success = all(
            plan_test.success for plan_test in test_result.plan_tests
        )

        return test_result

    def _validate_dr_plan(self, dr_plan: DRPlan) -> ValidationResult:
        """Validate DR plan completeness and accuracy."""
        validation_issues = []

        # Check required sections
        required_sections = [
            "assessment",
            "containment",
            "recovery",
            "restoration",
            "communication",
        ]
        for section in required_sections:
            if not hasattr(dr_plan, section) or not getattr(dr_plan, section):
                validation_issues.append(f"Missing required section: {section}")

        # Check contact information
        if not dr_plan.contacts or not dr_plan.escalation_contacts:
            validation_issues.append("Missing contact information")

        # Check RTO/RPO definitions
        if not dr_plan.rto_minutes or not dr_plan.rpo_minutes:
            validation_issues.append("Missing RTO/RPO definitions")

        # Check step dependencies
        for step in dr_plan.recovery_steps:
            for dependency in step.dependencies:
                if not any(s.name == dependency for s in dr_plan.recovery_steps):
                    validation_issues.append(
                        f"Step '{step.name}' has invalid dependency: {dependency}"
                    )

        return ValidationResult(
            success=len(validation_issues) == 0, issues=validation_issues
        )

    def generate_dr_report(self) -> DRReport:
        """Generate comprehensive disaster recovery report."""
        # Get current DR status
        dr_status = self._get_dr_status()

        # Calculate RTO/RPO compliance
        compliance_metrics = self._calculate_dr_compliance()

        # Get test results
        test_results = self._get_dr_test_results()

        # Generate recommendations
        recommendations = self._generate_dr_recommendations(
            dr_status, compliance_metrics, test_results
        )

        return DRReport(
            generated_at=datetime.utcnow(),
            dr_status=dr_status,
            compliance_metrics=compliance_metrics,
            test_results=test_results,
            recommendations=recommendations,
        )

    def _calculate_dr_compliance(self) -> DRComplianceMetrics:
        """Calculate disaster recovery compliance metrics."""
        compliance = DRComplianceMetrics()

        for dr_plan in self.dr_plans:
            plan_compliance = DRPlanCompliance(plan_name=dr_plan.name)

            # RTO compliance (based on test results)
            if dr_plan.rto_minutes:
                actual_rto = self._get_actual_rto(dr_plan.name)
                plan_compliance.rto_compliant = actual_rto <= dr_plan.rto_minutes

            # RPO compliance
            if dr_plan.rpo_minutes:
                actual_rpo = self._get_actual_rpo(dr_plan.name)
                plan_compliance.rpo_compliant = actual_rpo <= dr_plan.rpo_minutes

            # Backup compliance
            plan_compliance.backup_compliant = self._check_backup_compliance(dr_plan)

            # Overall plan compliance
            plan_compliance.overall_compliant = all([
                plan_compliance.rto_compliant,
                plan_compliance.rpo_compliant,
                plan_compliance.backup_compliant,
            ])

            compliance.plan_compliance.append(plan_compliance)

        # Calculate overall compliance
        compliant_plans = sum(
            1 for pc in compliance.plan_compliance if pc.overall_compliant
        )
        compliance.overall_compliance_percentage = (
            compliant_plans / len(compliance.plan_compliance)
        ) * 100

        return compliance

    def _generate_dr_recommendations(
        self, dr_status, compliance_metrics, test_results
    ) -> t.StringList:
        """Generate disaster recovery improvement recommendations."""
        recommendations = []

        # Compliance recommendations
        non_compliant_plans = [
            pc.plan_name
            for pc in compliance_metrics.plan_compliance
            if not pc.overall_compliant
        ]

        if non_compliant_plans:
            recommendations.append(
                f"Address compliance issues in DR plans: {', '.join(non_compliant_plans)}"
            )

        # Test recommendations
        failed_tests = [
            test.plan_name for test in test_results.plan_tests if test.failure
        ]

        if failed_tests:
            recommendations.append(
                f"Fix issues in failed DR plan tests: {', '.join(failed_tests)}"
            )

        # Status recommendations
        outdated_plans = [
            plan.name
            for plan in dr_status.dr_plans
            if (datetime.utcnow() - plan.last_updated).days > 90
        ]

        if outdated_plans:
            recommendations.append(
                f"Update outdated DR plans: {', '.join(outdated_plans)}"
            )

        if not recommendations:
            recommendations.append("DR capabilities are well-maintained and compliant")
            recommendations.append("Continue regular testing and updates")

        return recommendations```
______________________________________________________________________

## 🔧 Maintainability

### Maintainability Architecture

