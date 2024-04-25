
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: PropagateDataLinkParams</p>
 * <pre>
 * propagate_data_links parameters.
 *         id - the sample id.
 *         version - the sample version. (data links are propagated to)
 *         previous_version - the previouse sample version. (data links are propagated from)
 *         ignore_types - the workspace data type ignored from propagating. default empty.
 *         update - if false (the default), fail if a link already exists from the data unit (the
 *             combination of the UPA and dataid). if true, expire the old link and create the new
 *             link unless the link is already to the requested sample node, in which case the
 *             operation is a no-op.
 *         effective_time - the effective time at which the query should be run - the default is
 *             the current time. Providing a time allows for reproducibility of previous results.
 *         as_admin - run the method as a service administrator. The user must have full
 *             administration permissions.
 *         as_user - create the link as a different user. Ignored if as_admin is not true. Neither
 *             the administrator nor the impersonated user need have permissions to the data or
 *             sample.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "version",
    "previous_version",
    "ignore_types",
    "update",
    "effective_time",
    "as_admin",
    "as_user"
})
public class PropagateDataLinkParams {

    @JsonProperty("id")
    private java.lang.String id;
    @JsonProperty("version")
    private Long version;
    @JsonProperty("previous_version")
    private Long previousVersion;
    @JsonProperty("ignore_types")
    private List<String> ignoreTypes;
    @JsonProperty("update")
    private Long update;
    @JsonProperty("effective_time")
    private Long effectiveTime;
    @JsonProperty("as_admin")
    private Long asAdmin;
    @JsonProperty("as_user")
    private java.lang.String asUser;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public java.lang.String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(java.lang.String id) {
        this.id = id;
    }

    public PropagateDataLinkParams withId(java.lang.String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public PropagateDataLinkParams withVersion(Long version) {
        this.version = version;
        return this;
    }

    @JsonProperty("previous_version")
    public Long getPreviousVersion() {
        return previousVersion;
    }

    @JsonProperty("previous_version")
    public void setPreviousVersion(Long previousVersion) {
        this.previousVersion = previousVersion;
    }

    public PropagateDataLinkParams withPreviousVersion(Long previousVersion) {
        this.previousVersion = previousVersion;
        return this;
    }

    @JsonProperty("ignore_types")
    public List<String> getIgnoreTypes() {
        return ignoreTypes;
    }

    @JsonProperty("ignore_types")
    public void setIgnoreTypes(List<String> ignoreTypes) {
        this.ignoreTypes = ignoreTypes;
    }

    public PropagateDataLinkParams withIgnoreTypes(List<String> ignoreTypes) {
        this.ignoreTypes = ignoreTypes;
        return this;
    }

    @JsonProperty("update")
    public Long getUpdate() {
        return update;
    }

    @JsonProperty("update")
    public void setUpdate(Long update) {
        this.update = update;
    }

    public PropagateDataLinkParams withUpdate(Long update) {
        this.update = update;
        return this;
    }

    @JsonProperty("effective_time")
    public Long getEffectiveTime() {
        return effectiveTime;
    }

    @JsonProperty("effective_time")
    public void setEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public PropagateDataLinkParams withEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public PropagateDataLinkParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonProperty("as_user")
    public java.lang.String getAsUser() {
        return asUser;
    }

    @JsonProperty("as_user")
    public void setAsUser(java.lang.String asUser) {
        this.asUser = asUser;
    }

    public PropagateDataLinkParams withAsUser(java.lang.String asUser) {
        this.asUser = asUser;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((("PropagateDataLinkParams"+" [id=")+ id)+", version=")+ version)+", previousVersion=")+ previousVersion)+", ignoreTypes=")+ ignoreTypes)+", update=")+ update)+", effectiveTime=")+ effectiveTime)+", asAdmin=")+ asAdmin)+", asUser=")+ asUser)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
